import processing.net.*;

//Network
Server s;
Client c;

//Buttons
Button User_Motion_Button;
Button User_Throw_Button;
Button Computer_Throw_Button;
Button New_Player_Button;
Button Quit_Button;
  
//Global Variables
int Motion_Enable;
String User_Motion;
String User_Throw;
String Comp_Throw;

int transaction_number;

int timer;


//RECEIVE PACKETS TILL PACKET IDENTIFIER MATCHES EXPECTED
//--mouse
boolean clicked;

void setup()
{
  background(255,255,255);
  size(500,500);
  
  //Set frame rate
  frameRate(60);
  
  //Start Network
  s                  = new Server(this, 7000, "127.0.0.1");
  
  transaction_number = 0;
  timer              = 0;
  clicked            = false;
}

void draw()
{
  background(255,255,255);
  
  User_Motion_Button      = new Button(width/2, (height*1)/5 - 75, 100, 50, "Get User Motion", 10);
  User_Throw_Button       = new Button(width/2, (height*2)/5 - 75, 100, 50, "Get User Throw", 10);
  Computer_Throw_Button   = new Button(width/2, (height*3)/5 - 75, 100, 50, "Get Computer Throw", 10);
  New_Player_Button       = new Button(width/2, (height*4)/5 - 75, 100, 50, "Restart Comp", 10);
  Quit_Button             = new Button(width/2, (height*5)/5 - 75, 100, 50, "Quit", 10);
  
  textSize(25);
  fill(0,0,0);
  text(timer++, width/4, (height*3)/5 - 40); 
  
  if(User_Motion_Button.Click())
  {
     Motion_Enable = 1;
     thread("receiveUserMotion");
  }
  else if(User_Throw_Button.Click())
  {
     Motion_Enable = 0;
     transaction_number++;
     thread("receiveUserThrow");
  }
  else if(Computer_Throw_Button.Click())
  {
     Motion_Enable = 0;
     transaction_number++;
     thread("receiveComputerThrow");
  }
  else if(New_Player_Button.Click())
  {
     Motion_Enable = 0;
     transaction_number++;
     thread("setNewPlayer");
  }
  else if(Quit_Button.Click())
  {
     Motion_Enable = 0;
     exit();
  }

}

//MouseClicked
void mouseClicked()
{
   clicked = true;
}

void receiveUserMotion()
{  
   //Variable
   User_Motion = "00";
   String data_in="";
   
   //Network
   s.write("1");
   while(Motion_Enable == 1)
   {    
     //while(User_Motion.charAt(0) == '1'){
     c = s.available();
     if (c != null) {
       data_in     = c.readString();
       data_in     = data_in.substring(0, data_in.indexOf("\n"));
       User_Motion = data_in;
     }
     //}
     //Terminal
     transaction_number++;
     println("========================================");
     println("");
     print("==Received User Motion: ");
     println(User_Motion);
     print("(");
     print(transaction_number);
     println(")");
     println("========================================");
     println("");
     delay(500);
     
   }
   
}

void receiveUserThrow()
{  
   //Variable
   User_Throw = "00";
   String data_in="";
   
   //Network
   s.write("2");
   
   while(User_Throw.charAt(0) != '2'){
     c = s.available();
     if (c != null) {
       data_in     = c.readString();
       data_in     = data_in.substring(0, data_in.indexOf("\n"));
       User_Throw  = data_in;
     }
   }
   
   //Terminal
   println("========================================");
   println("");
   print("==Received User Throw: ");
   println(User_Throw);
   print("(");
   print(transaction_number);
   println(")");
   println("========================================");
   println("");
}

void receiveComputerThrow()
{  
   //Variable
   Comp_Throw = "00";
   String data_in="";
   
   //Network
   s.write("3");
   
   while(Comp_Throw.charAt(0) != '3'){
     c = s.available();
     if (c != null) {
       data_in     = c.readString();
       data_in     = data_in.substring(0, data_in.indexOf("\n"));
       Comp_Throw  = data_in;
     }  
   }
   
   //Terminal
   println("========================================");
   println("");
   print("==Received Computer Throw: ");
   println(Comp_Throw);
   print("(");
   print(transaction_number);
   println(")");
   println("========================================");
   println("");
}

void setNewPlayer()
{  
   //Network 
   s.write("4");
   
   //Terminal
   println("========================================");
   println("==Set New Game");
   print("(");
   print(transaction_number);
   println(")");
   println("========================================");
   println("");
}
