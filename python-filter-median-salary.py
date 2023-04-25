import csv

# Find time to make the zipcodes insert into the database
data = []
def read_csv():
    with open('zipcodes.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # get the header row
        zip_code_index = headers.index('NAME')  # find the index of the column
        # Estimate!!Median income (dollars)!!FAMILIES!!Families!!With own children of householder under 18 years
        median_income = headers.index('S1903_C03_016E')  # find the index of the column
        number_of_houses = headers.index('S1903_C02_034E')  # find the index of the column
        print(f"The column index of 'column_name' is {zip_code_index}")
        data.append(["zipcode", "median_salary", "number_of_houses"])
        count = 0
        for row in reader:
            ## This is so that we do not get weird headers in the csv file
            count += 1
            if count == 1:
                continue

            if row[median_income] == "250,000+":
                median_come = 250000
            elif row[median_income] == "-":
                median_come = 0
            else:
                median_come = row[median_income]
            data.append([row[zip_code_index].split(" ", 1)[1], median_come, row[number_of_houses]])
            # print(row[zip_code_index])
            # print(row[median_income])
            # print(row[number_of_houses])

def write_allzip_csv():
    with open('nj-median-salary.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)

read_csv()
write_allzip_csv()
print("here")
