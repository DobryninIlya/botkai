from .. import classes

cursor = classes.cursor
connection = classes.connection

def vkpay_transaction(request):
    object = data["object"]
        from_id = object["from_id"]
        amount = str(object["amount"])
        amount = amount[:-3] + "." + amount[-3:-1]
        sql = "SELECT balance FROM Users WHERE ID_VK=" + str(from_id) + ';'
        cursor.execute(sql)
        realAmount = cursor.fetchone()
        realAmount = realAmount[0]
        realAmount = (str(realAmount))[1:]
        amount = (float)(realAmount) + (float)(amount)
        #print("last" + str(amount))
        sql = "UPDATE Users SET balance=" + str(amount) + " WHERE ID_VK=" + str(from_id) + ';'
        cursor.execute(sql)
        connection.commit()

    return "ok"