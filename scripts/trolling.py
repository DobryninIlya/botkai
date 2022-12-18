i1=input("Введите минимальное количество знаков ")
i2=input("Введите максимальное количество знаков ")
for number in range(int(i1)-1, int(i2)):
    for x in range(pow(10, int(i1)-1), pow(10, int(i2))):
        grade = len(str(x))
        summ=0
        for num in range(0, grade): # Пробегаемся по каждому разряду в числе
            summ+=pow(int(str(x)[num]), grade)
        if summ==x:
            print(x)