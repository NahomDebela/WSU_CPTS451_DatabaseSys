import sys
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout
import psycopg2

qtCreatorFile = "milestone1App.ui"

Ui_MainWindow, QTBaseCLass = uic.loadUiType(qtCreatorFile)


class yelp_app(QMainWindow):
    def __init__(self):
        super(yelp_app, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.loadStateList()
        self.ui.stateList.currentTextChanged.connect(self.stateChanged)
        self.ui.cityList.itemSelectionChanged.connect(self.cityChanged)
        self.ui.cityList.itemSelectionChanged.connect(self.Zipcode)
        self.ui.Zipcode_list.itemSelectionChanged.connect(self.ZipcodeChanged)
        self.ui.Zipcode_list.itemSelectionChanged.connect(self.DisplayPopularBusinesses)
        self.ui.Zipcode_list.itemSelectionChanged.connect(self.Categories)
        self.ui.Category_list.itemSelectionChanged.connect(self.Category_changed)
        self.ui.Zipcode_list.itemSelectionChanged.connect(self.Zip_Statistics)
        self.ui.Zipcode_list.itemSelectionChanged.connect(self.Top_Categories)
        self.ui.enter_login.textChanged.connect(self.getUserNames)
        self.ui.Userid_list.itemSelectionChanged.connect(self.displayUserInfo)
        self.ui.Userid_list.itemSelectionChanged.connect(self.displayFriendList)
        self.ui.Userid_list.itemSelectionChanged.connect(self.displaySuggestedFriends)
        self.ui.Userid_list.itemSelectionChanged.connect(self.DisplayLatestTip)

    def executeQuery(self, sql_str):
        try:
            conn = psycopg2.connect(
                "dbname = 'Milestone3DBv1' user = 'postgres' host = 'localhost' password = 'password'")  # Placeholder
            print("executed")
        except:
            print("Unable to connect")
        cur = conn.cursor()
        cur.execute(sql_str)

        conn.commit()
        result = cur.fetchall()
        conn.close()
        return result

    def loadStateList(self):
        self.ui.stateList.clear()
        sql_str = "SELECT distinct state FROM business ORDER BY state;"
        try:
            results = self.executeQuery(sql_str)
            for row in results:
                self.ui.stateList.addItem(row[0])
        except:
            print("Query failed")
        self.ui.stateList.setCurrentIndex(-1)
        self.ui.stateList.clearEditText()

    def stateChanged(self):  # once you click on a state -> shows city and business

        state = self.ui.stateList.currentText()
        if (self.ui.stateList.currentIndex() >= 0):
            self.ui.cityList.clear()
            self.ui.businessTable.clear()
            sql_str = "SELECT distinct city FROM business WHERE state = '" + state + "' ORDER BY city;"
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.cityList.addItem(row[0])
            except:
                print("Query failed")

            for i in reversed(range(self.ui.businessTable.rowCount())):
                self.ui.businessTable.removeRow(i)
            sql_str = "SELECT name, address, city, stars, numcheckins , numtips FROM business WHERE state = '" + state + "' ORDER BY name;"
            try:
                results = self.executeQuery(sql_str)

                style = "::section {"" background-color: #f3f3f3; }"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name','Address' ,'City', 'Stars','Checkins','Reviews'])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0, 250)
                self.ui.businessTable.setColumnWidth(1, 250)
                self.ui.businessTable.setColumnWidth(2, 150)
                currentRowCount = 0
                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.businessTable.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))

                    currentRowCount += 1
            except:
                print("Query failed")


    def cityChanged(self):  # once you click on a city -> shows business

        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0):
            self.ui.businessTable.clear()
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()

            sql_str = "SELECT name, address, city, stars, numcheckins, numtips FROM business WHERE state = '" + state + "' AND city='" + city +  \
                      "' ORDER BY name ;"
            try:
                results = self.executeQuery(sql_str)

                style = "::section {"" background-color: #f3f3f3; }"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name','Address' ,'City', 'Stars','Checkins','Reviews'])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0, 250)
                self.ui.businessTable.setColumnWidth(1, 250)
                self.ui.businessTable.setColumnWidth(2, 150)
                currentRowCount = 0
                for row in results:

                    self.ui.businessTable.setItem(currentRowCount, 0, QTableWidgetItem(row[0]))
                    self.ui.businessTable.setItem(currentRowCount, 1, QTableWidgetItem(row[1]))
                    self.ui.businessTable.setItem(currentRowCount, 2, QTableWidgetItem(row[2]))
                    self.ui.businessTable.setItem(currentRowCount, 3, QTableWidgetItem(str(row[3])))
                    self.ui.businessTable.setItem(currentRowCount, 4, QTableWidgetItem(str(row[4])))
                    self.ui.businessTable.setItem(currentRowCount, 5, QTableWidgetItem(str(row[5])))
                    currentRowCount += 1

            except:
                print("Query failed")

    def Zipcode(self):  # Zipcode_list

        self.ui.Zipcode_list.clear()

        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0):
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            sql_str = "SELECT distinct postal_code FROM business WHERE state = '" + state + "' AND city='" + city + "' "
            currentRowCount = 0
            try:
                results = self.executeQuery(sql_str)
                style = "::section {"" background-color: #f3f3f3; }"
                self.ui.Zipcode_list.horizontalHeader().setStyleSheet(style)
                self.ui.Zipcode_list.setColumnCount(len(results[0]))
                self.ui.Zipcode_list.setRowCount(len(results))
                self.ui.Zipcode_list.setHorizontalHeaderLabels(['Zipcode'])
                self.ui.Zipcode_list.resizeColumnsToContents()

                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.Zipcode_list.setItem(currentRowCount, colCount, QTableWidgetItem(row[colCount]))
                    currentRowCount += 1
            except:
                print("Query failed")

    def ZipcodeChanged(self):  # Zipcode Changed -> Display New Business List
        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0) and (
                len(self.ui.Zipcode_list.selectedItems()) > 0):
            self.ui.businessTable.clear()
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            zipcode = self.ui.Zipcode_list.selectedItems()[0].text()

            sql_str = "SELECT name, address, city, stars, numcheckins , numtips FROM business WHERE state = '" + state + "' AND city ='" + city + "' AND \
            postal_code ='" + zipcode + "'  "
            try:
                results = self.executeQuery(sql_str)

                style = "::section {"" background-color: #f3f3f3; }"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name','Address' ,'City', 'Stars','Checkins','Reviews'])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0, 250)
                self.ui.businessTable.setColumnWidth(1, 250)
                self.ui.businessTable.setColumnWidth(2, 150)
                currentRowCount = 0
                for row in results:
                    self.ui.businessTable.setItem(currentRowCount, 0, QTableWidgetItem(row[0]))
                    self.ui.businessTable.setItem(currentRowCount, 1, QTableWidgetItem(row[1]))
                    self.ui.businessTable.setItem(currentRowCount, 2, QTableWidgetItem(row[2]))
                    self.ui.businessTable.setItem(currentRowCount, 3, QTableWidgetItem(str(row[3])))
                    self.ui.businessTable.setItem(currentRowCount, 4, QTableWidgetItem(str(row[4])))
                    self.ui.businessTable.setItem(currentRowCount, 5, QTableWidgetItem(str(row[5])))
                    currentRowCount += 1
            except:
                print("Query failed")

    def Categories(self):  # Category_list
        self.ui.Category_list.clear()
        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0) and (
                len(self.ui.Zipcode_list.selectedItems()) > 0):
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            zipcode = self.ui.Zipcode_list.selectedItems()[0].text()
            sql_str = "SELECT DISTINCT category_name FROM business, categories WHERE state = '" + state + "' AND city ='" + city + "' AND postal_code ='" + zipcode \
                      + "' AND business.business_id = categories.business_id ORDER BY category_name "
            results = self.executeQuery(sql_str)
            for row in results:
                self.ui.Category_list.addItem(row[0])
            try:
                style = "::section {"" background-color: #f3f3f3; }"
                self.ui.Category_list.horizontalHeader().setStyleSheet(style)
                self.ui.Category_list.setColumnCount(len(results[0]))
                self.ui.Category_list.setRowCount(len(results))
                self.ui.Category_list.setHorizontalHeaderLabels(['Categories'])
                self.ui.Category_list.resizeColumnsToContents()

                for row in results:
                    self.ui.Category_list.addItem(row[0])
            except:
                print("Query failed aa ")

    def Category_changed(self):  # Category_list
        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0) and (
                len(self.ui.Zipcode_list.selectedItems()) > 0) and (
                len(self.ui.Category_list.selectedItems()) > 0):
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            zipcode = self.ui.Zipcode_list.selectedItems()[0].text()
            category = self.ui.Category_list.selectedItems()[0].text()

            sql_str = "SELECT name, address, city, stars, numcheckins , numtips FROM business, categories WHERE state = '" + state + "' AND city ='" + city + "' AND postal_code ='" + zipcode \
                      + "' AND category_name = '" + category + "'  AND business.business_id = categories.business_id ORDER BY name; "

            results = self.executeQuery(sql_str)
            try:
                results = self.executeQuery(sql_str)
                style = "::section {"" background-color: #f3f3f3; }"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name','Address' ,'City', 'Stars','Checkins','Reviews'])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0, 250)
                self.ui.businessTable.setColumnWidth(1, 250)
                self.ui.businessTable.setColumnWidth(2, 150)

                currentRowCount = 0
                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.businessTable.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
            except:
                print("Query failed")

    def Zip_Statistics(self):  # Num_businesses
        self.ui.Num_businesses.clear()
        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0) and (
                len(self.ui.Zipcode_list.selectedItems()) > 0):
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            zipcode = self.ui.Zipcode_list.selectedItems()[0].text()
            sql_str = "SELECT COUNT(*) AS num_bus FROM (SELECT COUNT(business_id), business_id\
	        FROM business WHERE state = '" + state + "' AND city ='" + city + "' AND postal_code ='" + zipcode \
                      + "' GROUP BY(business_id)) AS derivedTable "
            results = self.executeQuery(sql_str)
            currentRowCount = 0
            for row in results:
                self.ui.Num_businesses.addItem(str(row[0]))

    def Top_Categories(self):  # Display Top categories table
        self.ui.Top_cat.clear()
        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0) and (
                len(self.ui.Zipcode_list.selectedItems()) > 0):
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            zipcode = self.ui.Zipcode_list.selectedItems()[0].text()
            sql_str = "SELECT category_name, COUNT(category_name) AS num_categories FROM Business, Categories WHERE " \
                      "state = '" + state + "' AND city ='" + city + "' AND postal_code ='" + zipcode \
                      + "' AND Business.business_id = Categories.business_id GROUP BY category_name ORDER" \
                        " BY COUNT(category_name) DESC; "
            results = self.executeQuery(sql_str)
            try:
                results = self.executeQuery(sql_str)
                style = "::section {"" background-color: #f3f3f3; }"
                self.ui.Top_cat.horizontalHeader().setStyleSheet(style)
                self.ui.Top_cat.setColumnCount(len(results[0]))
                self.ui.Top_cat.setRowCount(len(results))
                self.ui.Top_cat.setHorizontalHeaderLabels(['Amount', 'Category'])
                self.ui.Top_cat.resizeColumnsToContents()
                currentRowCount = 0
                for row in results:
                    self.ui.Top_cat.setItem(currentRowCount, 0, QTableWidgetItem(str(row[1])))
                    self.ui.Top_cat.setItem(currentRowCount, 1, QTableWidgetItem(row[0]))
                    currentRowCount += 1
            except:
                print("Query failed")

    def DisplayPopularBusinesses(self):  # Display Popular Businesses in zip code
        #self.ui.Popular_business.clear()
        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0) and (
                len(self.ui.Zipcode_list.selectedItems()) > 0):
            zipcode = self.ui.Zipcode_list.selectedItems()[0].text()

            sql_str = "SELECT Business.name, " \
                      "(((CAST(Business.review_count AS FLOAT) + CAST(Business.numtips AS FLOAT)) / Business.numcheckins) + " \
                      "(3.8416/(2*Business.numcheckins)) - (1.96 * SQRT(((((CAST(Business.review_count AS FLOAT) + " \
                      "CAST(Business.numtips AS FLOAT)) / Business.numcheckins)*(1 - ((CAST(Business.review_count AS FLOAT) + " \
                      "CAST(Business.numtips AS FLOAT)) / Business.numcheckins)) + (3.8416/(4*Business.numcheckins)))) / " \
                      "Business.numcheckins))) / (1 + (3.8416/Business.numcheckins)) AS pop_score FROM Business " \
                      "WHERE (CAST(Business.review_count AS FLOAT) + CAST(Business.numtips AS FLOAT)) < Business.numcheckins " \
                      "AND Business.numcheckins >= 25 AND Business.postal_code = '" + zipcode + "' ORDER BY pop_score DESC; "

            print(sql_str)

            try:
                results = self.executeQuery(sql_str)
                style = "::section {"" background-color: #f3f3f3; }"
                self.ui.Popular_business.horizontalHeader().setStyleSheet(style)
                self.ui.Popular_business.setColumnCount(len(results[0]))
                self.ui.Popular_business.setRowCount(len(results))
                self.ui.Popular_business.setHorizontalHeaderLabels(
                    ['Business Name', 'Popularity Score'])
                self.ui.Popular_business.setColumnWidth(0, 250)
                self.ui.Popular_business.setColumnWidth(1, 250)
                self.ui.Popular_business.setColumnWidth(2, 150)
                currentRowCount = 0
                for row in results:
                    self.ui.Popular_business.setItem(currentRowCount, 0, QTableWidgetItem(str(row[0])))
                    self.ui.Popular_business.setItem(currentRowCount, 1, QTableWidgetItem(str(row[1])))

                    currentRowCount += 1

            except:
                print("Query failed")

    def getUserNames(self):  # Enter User Login
        self.ui.Userid_list.clear()
        user_name = self.ui.enter_login.text()
        sql_str = "SELECT user_id FROM users WHERE name LIKE '%" + user_name + "%' ORDER BY name;"
        try:
            results = self.executeQuery(sql_str)
            for row in results:
                self.ui.Userid_list.addItem(row[0])
        except:
            print("Query failed")

    def displayUserInfo(self):  # Display user's name
        self.ui.display_user.clear()
        self.ui.display_stars.clear()
        self.ui.Yelp_since.clear()
        self.ui.funny_votes.clear()
        self.ui.cool_votes.clear()
        self.ui.useful_votes.clear()
        user_id = self.ui.Userid_list.selectedItems()[0].text()
        sql_str = "SELECT name FROM users WHERE user_id = '" + user_id + "';"
        try:
            results = self.executeQuery(sql_str)
            for row in results:
                self.ui.display_user.addItem(row[0])
        except:
            print("Query failed")

        # Display user's stars
        sql_str = "SELECT Users.average_stars FROM users WHERE Users.user_id = '" + user_id + "';"
        try:
            results = self.executeQuery(sql_str)
            for row in results:
                self.ui.display_stars.addItem(str(row[0]))
        except:
            print("Query failed")

        # Display user's Yelping Date
        sql_str = "SELECT Users.yelping_since FROM users WHERE Users.user_id = '" + user_id + "';"
        try:
            results = self.executeQuery(sql_str)
            for row in results:
                self.ui.Yelp_since.addItem(str(row[0]))
        except:
            print("Query failed")

        # Display user's funny Votes
        sql_str = "SELECT Users.funny FROM users WHERE Users.user_id = '" + user_id + "';"
        try:
            results = self.executeQuery(sql_str)
            for row in results:
                self.ui.funny_votes.addItem(str(row[0]))
        except:
            print("Query failed")

        # Display user's cool Votes
        sql_str = "SELECT Users.cool FROM users WHERE Users.user_id = '" + user_id + "';"
        try:
            results = self.executeQuery(sql_str)
            for row in results:
                self.ui.cool_votes.addItem(str(row[0]))
        except:
            print("Query failed")

        # Display user's useful Votes
        sql_str = "SELECT Users.useful FROM users WHERE Users.user_id = '" + user_id + "';"
        try:
            results = self.executeQuery(sql_str)
            for row in results:
                self.ui.useful_votes.addItem(str(row[0]))
        except:
            print("Query failed")

    def displayFriendList(self):  # friend_table
        # Display Users Friends
        self.ui.friend_table.clear()
        self.ui.friend_table.setHorizontalHeaderLabels(
            ['Name', 'Average Stars', 'Fans', 'Tip Count', 'Yelping Since'])
        if (len(self.ui.Userid_list.selectedItems()) > 0):
            user_id = self.ui.Userid_list.selectedItems()[0].text()

            sql_str = "SELECT Users.name, Users.average_stars, Users.fans, Users.tip_count, Users.yelping_since " \
                      "FROM (SELECT Friend.friend_id FROM Friend WHERE Friend.user_id = '" + user_id + "' ) " \
                      "AS user_friends INNER JOIN Users ON user_friends.friend_id = Users.user_id ORDER BY Users.average_stars DESC;"
            try:
                results = self.executeQuery(sql_str)
                style = "::section {"" background-color: #f3f3f3; }"
                self.ui.friend_table.horizontalHeader().setStyleSheet(style)
                self.ui.friend_table.setColumnCount(len(results[0]))
                self.ui.friend_table.setRowCount(len(results))
                self.ui.friend_table.setHorizontalHeaderLabels(
                    ['Name', 'Average Stars', 'Fans', 'Tip Count', 'Yelping Since'])

                currentRowCount = 0
                for row in results:
                    self.ui.friend_table.setItem(currentRowCount, 0, QTableWidgetItem(row[0]))
                    self.ui.friend_table.setItem(currentRowCount, 1, QTableWidgetItem(str(row[1])))
                    self.ui.friend_table.setItem(currentRowCount, 2, QTableWidgetItem(str(row[2])))
                    self.ui.friend_table.setItem(currentRowCount, 3, QTableWidgetItem(str(row[3])))
                    self.ui.friend_table.setItem(currentRowCount, 4, QTableWidgetItem(str(row[4])))
                    currentRowCount += 1
            except:
                print("Query failed")

    def displaySuggestedFriends(self):  # friend_table

        # Display Users Suggested Friends
        self.ui.friend_suggestions.clear()
        self.ui.friend_suggestions.setHorizontalHeaderLabels(
            ['Name', 'Average Stars', 'Fans', 'Tip Count', 'Yelping Since'])
        if (len(self.ui.Userid_list.selectedItems()) > 0):
            print("hey")
            user_id = self.ui.Userid_list.selectedItems()[0].text()
            sql_str = "SELECT Users.name, Users.average_stars, Users.fans, Users.tip_count, Users.yelping_since FROM " \
            "(" \
            "SELECT DISTINCT Friend.friend_id AS friends_of_friends_id FROM" \
            "(" \
            "SELECT Friend.friend_id AS my_friends_id FROM Friend WHERE Friend.user_id = '" + user_id + "' " \
            ")"\
            "AS my_friends" \
            " INNER JOIN Friend ON my_friends.my_friends_id = Friend.user_id EXCEPT" \
            " SELECT Friend.friend_id FROM Friend WHERE Friend.user_id = '" + user_id + "' " \
            ")" \
            "AS Ftbl INNER JOIN Users ON Ftbl.friends_of_friends_id = Users.user_id ORDER BY Users.average_stars DESC;"

            try:
                results = self.executeQuery(sql_str)
                print(results)
                style = "::section {"" background-color: #f3f3f3; }"
                self.ui.friend_suggestions.horizontalHeader().setStyleSheet(style)
                self.ui.friend_suggestions.setColumnCount(len(results[0]))
                self.ui.friend_suggestions.setRowCount(len(results))
                self.ui.friend_suggestions.setHorizontalHeaderLabels(
                    ['Name', 'Average Stars', 'Fans', 'Tip Count', 'Yelping Since'])
                currentRowCount = 0
                for row in results:
                    self.ui.friend_suggestions.setItem(currentRowCount, 0, QTableWidgetItem(row[0]))
                    self.ui.friend_suggestions.setItem(currentRowCount, 1, QTableWidgetItem(str(row[1])))
                    self.ui.friend_suggestions.setItem(currentRowCount, 2, QTableWidgetItem(str(row[2])))
                    self.ui.friend_suggestions.setItem(currentRowCount, 3, QTableWidgetItem(str(row[3])))
                    self.ui.friend_suggestions.setItem(currentRowCount, 4, QTableWidgetItem(str(row[4])))
                    currentRowCount += 1
            except:
                print("Query failed")

    def DisplayLatestTip(self):  # Display Users Friends
        self.ui.latest_tips.clear()
        self.ui.latest_tips.setHorizontalHeaderLabels(['Name', 'Business', 'City', 'Date', 'Review'])
        if len(self.ui.Userid_list.selectedItems()) > 0:
            user_id = self.ui.Userid_list.selectedItems()[0].text()
            sql_str = "SELECT DISTINCT ON (Ntbl.user_id) Ntbl.name, Btbl.name, Btbl.city, Tip.date, Tip.text FROM " \
                      "(" \
                      "SELECT Users.user_id, Users.name FROM Users INNER JOIN " \
                      "( SELECT Friend.friend_id FROM Friend WHERE Friend.user_id = '" + user_id + "' )" \
                      "AS Ftbl ON Ftbl.friend_id = Users.user_id " \
                      ") AS Ntbl" \
                      " INNER JOIN Tip ON Ntbl.user_id = Tip.user_id INNER JOIN " \
                      "( SELECT Business.business_id, Business.name, " \
                      "Business.city FROM Business " \
                      ") AS Btbl ON Tip.business_id = Btbl.business_id ORDER BY Ntbl.user_id, Tip.date DESC; "
            try:
                results = self.executeQuery(sql_str)
                style = "::section {"" background-color: #f3f3f3; }"
                self.ui.latest_tips.horizontalHeader().setStyleSheet(style)
                self.ui.latest_tips.setColumnCount(len(results[0]))
                self.ui.latest_tips.setRowCount(len(results))
                self.ui.latest_tips.setHorizontalHeaderLabels(['Name', 'Business', 'City', 'Date', 'Review'])
                currentRowCount = 0
                for row in results:
                    self.ui.latest_tips.setItem(currentRowCount, 0, QTableWidgetItem(row[0]))
                    self.ui.latest_tips.setItem(currentRowCount, 1, QTableWidgetItem(row[1]))
                    self.ui.latest_tips.setItem(currentRowCount, 2, QTableWidgetItem(row[2]))
                    self.ui.latest_tips.setItem(currentRowCount, 3, QTableWidgetItem(str(row[3])))
                    self.ui.latest_tips.setItem(currentRowCount, 4, QTableWidgetItem(row[4]))
                    currentRowCount += 1
            except:
                print("Query failed")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = yelp_app()
    # window.loadStateList()
    window.show()
    sys.exit(app.exec_())
