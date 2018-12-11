


sql_user = '''
    CREATE TABLE User(
        UserID varchar(32) PRIMARY KEY NOT NULL,
        Password varchar(64) NOT NULL,
        Address varchar(512) NOT NULL,
        Phone varchar(32) NOT NULL,
        IDNumber varchar(64) NOT NULL,
        Name varchar(16) NOT NULL
    );
    '''

sql_admin = '''
    CREATE TABLE Admin(
        AdminID varchar(16) PRIMARY KEY NOT NULL,
        Password varchar(64) NOT NULL
    );
    '''

sql_book = '''
    CREATE TABLE Book(
        BookID varchar(128) PRIMARY KEY NOT NULL,
        Name varchar(128) NOT NULL,
        Price numeric(16,4) NOT NULL,
        Detail varchar(2048),
        ISBN varchar(64),
        Number varchar(16) NOT NULL,
        Picture varchar(256),
        State varchar(16) NOT NULL,
        Author varchar(64),
        Class varchar(32)
    );
    '''


sql_orders = '''
    CREATE TABLE Orders(
        BookID varchar(128) NOT NULL,
        OrderID varchar(256) NOT NULL,
        Time varchar(32) NOT NULL,
        Number varchar(16) NOT NULL,
        Total numeric(16,4) NOT NULL,
        State varchar(16) NOT NULL,
        PRIMARY KEY(BookID,OrderID)
    );
    '''

sql_user_admin = '''
    CREATE TABLE User_Admin(
        UserID varchar(32) PRIMARY KEY NOT NULL,
        AdminID varchar(16) NOT NULL,
        FOREIGN KEY(AdminID) REFERENCES Admin(AdminID)
    );
    '''

sql_book_admin = '''
    CREATE TABLE Book_Admin(
        BookID varchar(128) PRIMARY KEY NOT NULL,
        AdminID varchar(16) NOT NULL,
        FOREIGN KEY(AdminID) REFERENCES Admin(AdminID)
    );
    '''

sql_user_book_lookup = '''
    CREATE TABLE User_Book_LookUp(
        BookID varchar(128) PRIMARY KEY NOT NULL,
        UserID varchar(32) NOT NULL,
        Time varchar(32) NOT NULL,
        FOREIGN KEY(UserID) REFERENCES User(UserID)
    );
    '''

sql_user_book_collect = '''
    CREATE TABLE User_Book_Collect(
        BookID varchar(128) PRIMARY KEY NOT NULL,
        UserID varchar(32) NOT NULL,
        Time varchar(32) NOT NULL,
        FOREIGN KEY(UserID) REFERENCES User(UserID)
    );
    '''

sql_user_book_publish = '''
    CREATE TABLE User_Book_Publish(
        BookID varchar(128) PRIMARY KEY NOT NULL,
        UserID varchar(32) NOT NULL,
        Time varchar(32) NOT NULL,
        FOREIGN KEY(UserID) REFERENCES User(UserID)
    );
    '''

sql_user_order = '''
    CREATE TABLE User_Order(
        BookID varchar(128) NOT NULL,
        OrderID varchar(256) NOT NULL,
        BuyerID varchar(32) NOT NULL,
        SellerID varchar(32) NOT NULL,
        PRIMARY KEY(BookID,OrderID),
        FOREIGN KEY(BuyerID) REFERENCES User(UserID),
        FOREIGN KEY(SellerID) REFERENCES User(UserID)
    );
    '''
