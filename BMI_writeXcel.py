from __future__ import print_function
from googleapiclient.discovery import build
from google.oauth2 import service_account


def write_excel(anganwaadi,name2,age2,wt,ht,bmi,status):
    SERVICE_ACCOUNT_FILE = 'keys.json'

    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = None
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # The ID of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = '1ANe6mCbfBotxoPYxlE9LTqaozV9EXsu024txCVlHzNU'

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range="Sheet1!A2:G2").execute()

    values = result.get('values', [])

    worksheet_name = 'Sheet1!'
    cell_range_insert = 'A2'

    # print(values)
    health_values = [[anganwaadi,name2,age2,wt,ht,bmi,status]]
    value_range_body = {
        'majorDimension': 'ROWS',
        'values': health_values
    }
    service.spreadsheets().values().append(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        valueInputOption='USER_ENTERED',
        range=worksheet_name + cell_range_insert,
        body=value_range_body
    ).execute()
    '''
    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[0], row[4]))

    '''


'''
if __name__ == "__main__":
    p1="Chattabi"
    p2="joint pains"
    p3="Artheries"
    p4="KPHosp"
    write_excel(p1,p2,p3,p4)
'''
