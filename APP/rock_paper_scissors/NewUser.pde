class NewUser
{
 
  int animation_int_time;
  int animation_gran;
  int animation_count = 0;
  
  NewUser()
  {
    animation_int_time = millis();
    animation_gran = 3000;
  }
  
  void draw()
  {
    thread("setNewPlayer");
    New_User_Enable = 0;
    fill(0,0,0);
    text("NEW PLAYER", width/2, height/2, 128);
    if(millis() > animation_int_time + animation_gran)
    {
       menu.reset();
       Current_Screen = 0;
    }
    
  }
  
  void reset()
  {
     animation_int_time = millis();
     animation_gran = 3000;
  }
 
}
