//MySQL連線測試，手動寫入一個溫度及濕度資料做測試
#include <WiFi.h>
#include <MySQL_Connection.h>
#include <MySQL_Cursor.h>

const char ssid[]     = "Galaxy A33 5G 2E47";// change to your WIFI SSID
const char password[] = "evgf4802";// change to your WIFI Password
IPAddress server_addr(192,168,102,52);// change to you server ip, note its form split by "," not "."
int MYSQLPort =3306;   //mysql port default is 3306
char user[] = "root";// Your MySQL user login username(default is root),and note to change MYSQL user root can access from local to internet(%)
char pass[] = "SQLpassword";// Your MYSQL password

WiFiClient client;            
MySQL_Connection conn((Client *)&client);

void setup() {
  Serial.begin(115200);
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  
  WiFi.begin(ssid, password);  
  //try to connect to WIFI 
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");  
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  
  //try to connect to mysql server
  if (conn.connect(server_addr, 3306, user, pass)) {
     delay(1000);
  }
  else{
    Serial.println("Connection failed.");
  }
  delay(2000);  
  //insert, change database name and values by string and char[]
  char INSERT_SQL[] = "INSERT INTO person.check (id,username,timestamp,status,time_period) VALUES ('0','林逸丞','2025-04-24 11:07:36','1','morning')";//傳入的值固定為溫度,濕度為35,60
  MySQL_Cursor *cur_mem = new MySQL_Cursor(&conn);  
  cur_mem->execute(INSERT_SQL);//execute SQL
  delete cur_mem;
  conn.close();                  // close the connection
  Serial.println("Data Saved.");
}

void loop() {
//do nothing
}