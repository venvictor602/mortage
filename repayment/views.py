import openpyxl
from django.shortcuts import render
from .forms import RepaymentForm
from django.http import HttpResponse, FileResponse
import os
from django.conf import settings

# Path to the template file
TEMPLATE_FILE_PATH = os.path.join(settings.BASE_DIR, 'repayment', 'files', 'our_template.xlsx')

def process_repayment(request):
    if request.method == 'POST':
        form = RepaymentForm(request.POST, request.FILES)
        if form.is_valid():
            akpab_file = request.FILES['akpab_file']
            selected_month = form.cleaned_data['month']
            selected_year = form.cleaned_data['year']  # Get the year from the form

            # Get the last two digits of the year
            last_two_digits_year = str(selected_year)[-2:]

            # Load AKPAB workbook
            akpab_wb = openpyxl.load_workbook(akpab_file)
            akpab_ws = akpab_wb.active

            # Load our template workbook
            template_wb = openpyxl.load_workbook(TEMPLATE_FILE_PATH)
            template_ws = template_wb.active

            # AKPAB file headers
            akpab_employee_number_col = 3  # EMPLOYMENT NUMBER is in column 3
            akpab_employee_name_col = 5    # EMPLOYEE NAME is in column 5
            akpab_amount_col = 6           # AMOUNT is in column 6

            # Find "TOTAL" column in the template and insert new month/year column before it
            total_column = None
            header_row = 3  # Assuming the template headers are in row 3

            for col in range(1, template_ws.max_column + 1):
                header_value = template_ws.cell(row=header_row, column=col).value
                if header_value == 'TOTAL':  # Find the 'TOTAL' column
                    total_column = col
                    break

            if total_column:
                # Create a new header combining the month and last two digits of the year
                new_month_year_column_name = f"{selected_month} {last_two_digits_year}"

                # Insert the new column before the "TOTAL" column
                template_ws.insert_cols(total_column)
                template_ws.cell(row=header_row, column=total_column, value=new_month_year_column_name)

                # Map rows from AKPAB to the template based on employee number and name
                for akpab_row in akpab_ws.iter_rows(min_row=4):  # AKPAB starts from row 4
                    akpab_employee_number = akpab_row[akpab_employee_number_col - 1].value
                    akpab_employee_name = akpab_row[akpab_employee_name_col - 1].value
                    akpab_amount = akpab_row[akpab_amount_col - 1].value

                    if akpab_employee_number and akpab_employee_name:
                        # Loop through template rows to match the employee
                        for template_row in range(3, template_ws.max_row + 1):
                            template_employee_number = template_ws.cell(row=template_row, column=3).value  # EMP_CODE
                            template_employee_name = template_ws.cell(row=template_row, column=4).value    # EMP_NAME

                            if template_employee_number == akpab_employee_number and template_employee_name == akpab_employee_name:
                                # Add the amount in the new month/year column
                                template_ws.cell(row=template_row, column=total_column, value=akpab_amount)

                                # Update total (now shifted one column right)
                                total_cell = template_ws.cell(row=template_row, column=total_column + 1)
                                total_cell.value = (total_cell.value or 0) + akpab_amount
                                break

            # Overwrite and save the modified template to the same file
            template_wb.save(TEMPLATE_FILE_PATH)

            # Prepare the filename using the selected month and last two digits of the year
            downloaded_filename = f"updated_template_{selected_month}_{last_two_digits_year}.xlsx"
            
            # Return the updated file as a response
            with open(TEMPLATE_FILE_PATH, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = f'attachment; filename={downloaded_filename}'
                return response

    else:
        form = RepaymentForm()

    return render(request, 'upload.html', {'form': form})



from django.http import FileResponse, HttpResponse
import os
from django.conf import settings

def download_template(request):
    # Define the template file path
    TEMPLATE_FILE_PATH = os.path.join(settings.BASE_DIR, 'repayment', 'files', 'our_template.xlsx')

    # Log the path for debugging
    print("Looking for template file at:", TEMPLATE_FILE_PATH)

    # Check if the template file exists
    if os.path.exists(TEMPLATE_FILE_PATH):
        # Use FileResponse to return the file
        return FileResponse(open(TEMPLATE_FILE_PATH, 'rb'), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    else:
        # Log the issue or provide more detail in the response
        return HttpResponse(f"Template file not found at {TEMPLATE_FILE_PATH}.", status=404)
