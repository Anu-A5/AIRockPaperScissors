import processing.net.*;

//PImages
PShape Rock;
PShape Paper;
PImage Scissors;
PImage Warning;
int Throw_Width;
int Throw_Height;

//PFonts
PFont font;

//Network
Server s;
Client c;
//Global Variables
int Motion_Enable;
int Comp_Throw_Enable;
int New_User_Enable;
String User_Motion;
String User_Throw;
String Comp_Throw;
boolean connected;
boolean disconnected;

int transaction_number;


//Screens
Menu       menu     = new Menu();
Run_Game   run_game = new Run_Game();
Results    stats    = new Results();
NewUser    new_user = new NewUser();

int Current_Screen;

//Game
String user_hands;
boolean shoot_flag;
String user_throw;
String computer_throw;
String outcome;

boolean CHEAT;

void setup()
{
  fullScreen(1);
  //size(800,800);
  exec("python", "C:/Users/anuhg/Documents/summer_projects/20232024/Projects/Rock_Paper_Scissors/RPS_BRAIN/rps_brain.py");
  //Load images (svgs)
  Rock      = loadShape("assets/Screens/Run_Game/rock.svg");
  Paper     = loadShape("assets/Screens/Run_Game/paper.svg");
  Scissors  = loadImage("assets/Screens/Run_Game/scissors.png");
  Warning   = loadImage("assets/Screens/Run_Game/warning.jpg");
  
  //resize
  //card_width  = width/3-50;
  //card_height = round(card_width * 1.23); 
  //Rock_Card.resize(card_width, card_height);
  
  Comp_Throw = "30";
  User_Motion= "10";
  User_Throw = "20";
      
  //Set frame rate
  frameRate(24);
  
  //Start Network
  s = new Server(this, 7000, "127.0.0.1");
  
  //Set initial screen
  Current_Screen = 0;
  
  connected=false;
  disconnected=false;
  
  font = createFont("assets/Fonts/no-continue.regular.ttf",128);
  textFont(font);
}

void draw()
{
  background(255,255,255);
  
  switch(Current_Screen)
  {
    case(0):
       menu.draw();
       break;
    case(1):
       run_game.draw();
       break;
    case(2):
       stats.draw();
       break;
    case(3):
       new_user.draw();
       break;
     default:
       menu.draw();
       break;   
  }
  
  fill(0,255,0);
  textSize(30);
  println(disconnected);
  if(connected && (Current_Screen==0)){text("Connected", width/20, height*9/10);}
  else if(disconnected && (Current_Screen==0)){
    fill(255,0,0);
    text("Connected", width/20, height*9/10);
  }
  else if(disconnected && (Current_Screen!=0)){
    fill(255,0,0);
    text("Connected", width*19/20, height*9/10);
  }
  fill(255,255,255);
  

}

void keyPressed() {
  if (key == 'r') {
    new_user.reset();
    Current_Screen = 3;
  } 
  if (key == 'm') {
    menu.reset();
    Current_Screen = 0;
  } 
  if (key == 'c') {
    CHEAT = true;
  } else {
    CHEAT = false;
  }
}



//Network
void serverEvent(Server someServer, Client someClient) {
  connected=true;
  disconnected=false;
}

void disconnectEvent(Client someClient){
  disconnected=true; 
  connected=false;
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
     delay(300);
     
   }
   
}

void receiveComputerThrow()
{  
   //Variable
   Comp_Throw = "00";
   String data_in="";
   
   //Network
   s.write("3");
   
   if(Comp_Throw_Enable == 1){
     while(Comp_Throw.charAt(0) != '3'){
       c = s.available();
       if (c != null) {
         data_in     = c.readString();
         data_in     = data_in.substring(0, data_in.indexOf("\n"));
         Comp_Throw  = data_in;
       }  
     }
     
   }
   Comp_Throw_Enable = 0;
   Motion_Enable = 1;
   
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

void setNewPlayer()
{  
   if(New_User_Enable == 1)
   {
     //Network 
     s.write("4");
   }
   
   //Terminal
   println("========================================");
   println("==Set New Game");
   print("(");
   print(transaction_number);
   println(")");
   println("========================================");
   println("");
}
