/**
* @brief Demo for WiFi AP mode and web server
* 
* Instructions: Modify the demo (including the callbacks), configure AP and run.
* 
* @author Oscar Diaz <odiaz@ieee.org>
*/

// Required headers
#include <WiFi.h>
#include <WiFiAP.h>
#include <WebServer.h>

// Credentials
const char * ap_ssid = "mydemoAP";  ///< Network name
const char * ap_password = "";      ///< Network password (use empty to open network)
const int server_port = 80;         ///< Webserver port

// Resources
WebServer myserver(server_port);

// web pages

/**
* @brief Handler for root page (index.html)
*/
void handleRoot() 
{
  Serial.println("Root page requested");
  // Put here any actions to do before 
  // generating this page
  // ****

  // Page content
  String content = \
  "<html>\
    <head>\
      <title>ESP32 Webserver Demo</title>\
    </head>\
    <body>\
      <h1>Hello from ESP32!</h1>\
      <p><a href=\"/demo\">See this demo page too.</a></p>\
    </body>\
  </html>";

  // send response
  myserver.send(200, "text/html", content);

  Serial.println("Root page sent");
}

/**
* @brief Handler for demo page
*/
void handleDemo() 
{
  Serial.println("Demo page requested");

  // Put here any actions to do before 
  // generating this page
  // ****

  // Page content
  String content = \
  "<html>\
    <head>\
      <title>ESP32 Webserver Demo</title>\
    </head>\
    <body>\
      <h1>This is another demo page</h1>\
      <p><a href=\"/\">Back to index.</a></p>\
    </body>\
  </html>";

  // send response
  myserver.send(200, "text/html", content);
  Serial.println("Demo page sent");
}

/**
* @brief Handler for not found case
*/
void handleNotFound() 
{
  Serial.print("Notfound detected to: ");
  Serial.println(myserver.uri());
  // Put here any actions to do before 
  // generating this page
  // ****

  // Page content (header)
  String content = \
  "<html>\
    <head>\
      <title>Not found</title>\
    </head>\
    <body>";
  // specific content
  content += "<h1>Resource not found: ";
  content += myserver.uri();
  content += "</h1>";
  // Page content (footer)
  content += "</body></html>";

  // send response
  myserver.send(404, "text/html", content);
  Serial.println("Notfound sent");
}

/**
* @brief Arduino initialization
*/
void setup() 
{
  // Console initialization
  Serial.begin(115200);
  Serial.println("Starting...");

  // AP initialization
  if (strlen(ap_password) == 0)
  {
    Serial.println("No password, open AP");
    if (!WiFi.softAP(ap_ssid)) 
    {
      // error reported, cannot continue
      Serial.println("Soft AP (no password) creation failed.");
      while (1);
    }
  }
  else
  {
    Serial.println("Password enabled AP");
    if (!WiFi.softAP(ap_ssid, ap_password)) 
    {
      // error reported, cannot continue
      Serial.println("Soft AP (with password) creation failed.");
      while (1);
    }
  }
  
  // get the current IP address and show on console
  IPAddress myIP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(myIP);

  // Web server handlers, add all handlers required
  myserver.on("/", handleRoot);
  myserver.on("/demo", handleDemo);
  myserver.onNotFound(handleNotFound);

  // Start web server
  myserver.begin();
  Serial.println("HTTP server started");
}

/**
* @brief Arduino loop
*/
void loop() 
{
  // Put here any actions to do periodically
  // ****

  // Web server handler, do not remove
  myserver.handleClient();
  delay(100);  //allow the cpu to switch to other tasks
}
