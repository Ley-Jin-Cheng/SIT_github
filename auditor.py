total_inventory=0
failed_entries=0

while True:
    stock=input ("Enter stock quantity or quit to exit:")


    if stock == "quit":
        break

    if stock.isdigit()==False:
        print("Enter a valid number")
        failed_entries +=1
        continue


    stock =int(stock)

    if stock < 0 :
        print("Value cannot be less than 0")
        failed_entries +=1
        continue

    total_inventory= total_inventory+stock

    stock=str(stock)

    print("Added "+stock +" to total inventory")

    if total_inventory>500:
        print("Total inventory exceded 500")
        break


total_inventory=str(total_inventory)
failed_entries=str(failed_entries)


print("Total unit Processed is "+ total_inventory)
print("Total fail/rejected entries "+failed_entries)