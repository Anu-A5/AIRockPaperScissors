class Menu
{
  Button Start_Button;
  Button Quit_Button;
  
  String data_out;
  
  int animation_int_time;
  int animation_c_img;
  
  Menu()
  {
    animation_int_time = millis();
    animation_c_img = 0;
  }
  
  void draw()
  {
    int animation_gran  = 5000;
    int animation_x = ((width*1)/6);
    int animation_y = height/12;
    int animation_w = width/2;
    int animation_h = animation_w;
    
    if(millis() > animation_int_time + animation_gran)
    {
       animation_c_img++;
       animation_int_time = millis();
       
       if(animation_c_img >= 3)
         {
            animation_c_img = 0;
         }
    }
    
    rectMode(CENTER);
    switch(animation_c_img)
    {
       case(0):
          shape(Rock, animation_x, animation_y, animation_w, animation_h);
          break;
       case(1):
          shape(Paper, animation_x, animation_y, animation_w, animation_h);
          break;
       case(2):
          image(Scissors, animation_x, animation_y, animation_w, animation_h);
          break;
        default:
          shape(Rock, animation_x, animation_y, animation_w, animation_h);
          break;  
    }
    //Title Screen
    //image(Menu_Title, width/2-500, (height)/4);// I want this to grow in and shrink in size continously
    stroke(0,0,0);
    //Navigation Buttons
    this.Start_Button = new Button((width*5/6) - 100, (height*2)/6     , 200, 100, "START", 100);
    strokeWeight(5);
    line((width*5/6) - 75, (height*2)/6 + 100, (width*5/6) + 75, (height*2)/6 + 100);
    
    this.Quit_Button = new Button((width*5/6) - 100, (height*2)/6 + 325, 200, 100, "QUIT", 100);
    strokeWeight(5);
    line((width*5/6) - 75, (height*2)/6 + 425, (width*5/6) + 75, (height*2)/6 + 425);
    
    //Button Functionality
    if(Start_Button.Click()){
      run_game.reset();
      Current_Screen++;
    }
    if(Quit_Button.Click()){
      s.stop();
      exit();
    }
    
  }
  
  void reset()
  {
     animation_int_time = millis();
     animation_c_img = 0;
     New_User_Enable = 1;
  }
  
}
