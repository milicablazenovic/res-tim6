import statistics
while True:
    print("1. Izvestaj o potrosnji po mesecima za odredjeni grad.")
    print("2. Izvestaj o potrosnji po mesecima za odredjeno brojilo.")
    print("3. Izlaz")

    unos = input()

    if unos == '1':
        statistics.potrosnjaGrad()
    elif unos == '2':
        statistics.potrosnjaBrojila()
    elif unos == '3':
        exit()
    else:
        print("Unesite broj od 1-3!")

