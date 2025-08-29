class Run_Game
{
  String data_out;
  Button Stop;
  
  //threads
  int started_move;
  int started_comp;
  
  int animation_int_time;
  int animation_gran;
  int animation_count = 0;
  
  int curr_throw;
  
  
  Run_Game()
  {
    started_move = 0;
    started_comp = 0;
    animation_int_time = millis();
    animation_gran = 1000;
    animation_count = 0;
    curr_throw = 0;
  }
  
  void draw()
  {
    int animation_x = ((width*1)/4);
    int animation_y = height/12;
    int animation_w = width/2;
    int animation_h = animation_w;
    int count_down_length = 3;
    
    
    //start a thread that continously gets user hand gesture from camera
    
    //draw assets
    rectMode(CENTER);
    
    //start threads
    if((Comp_Throw_Enable == 1) &&(started_comp == 0))
    {
       thread("receiveComputerThrow");
       started_comp=1;
    }
    
    if((Motion_Enable == 1) && (started_move == 0))
    {
       thread("receiveUserMotion");
       started_move=1;
    }
    
    //Display
    int current_throw = User_Motion.charAt(1) - 48;

    switch(current_throw) //pause timer till current throw != 0
    {
       case(1):
         shape(Rock, animation_x, animation_y, animation_w, animation_h);
         curr_throw = 1;
         break;
       case(2):
         shape(Paper, animation_x, animation_y, animation_w, animation_h);
         curr_throw = 2;
         break;
       case(3):
         image(Scissors, animation_x, animation_y, animation_w, animation_h);
         curr_throw = 3;
         break;
       case(0):
         image(Warning, animation_x, animation_y, animation_w, animation_h);
         curr_throw = 0;
         fill(255,142,97);
         textSize(150);
         text("ADJUST", width*5/6, height*3/6);
         break;   
    }
    
    textAlign(CENTER);
    textSize(50);
    fill(0,0,0);
    text("Your Throw ...",width/2, height-50);
    
    //Do rock paper scissor animation.
    if((millis() > animation_int_time + animation_gran) && (curr_throw!=0))
    {
       animation_int_time = millis();
       animation_count++;
    }
    
    textSize(100);
    fill(255,142,97);
    text(count_down_length-animation_count, width*5/6, height*1/6);
   
    if((count_down_length-animation_count)==0){
      Motion_Enable = 0;
      receiveUserThrow();
      stats.reset();
      Current_Screen++;
    }
    
  }

  void reset()
  {
     started_move = 0;
     started_comp = 0;
     Motion_Enable = 0;
     curr_throw = 0;
     Comp_Throw_Enable = 1;
     animation_int_time = millis();
     animation_gran = 1000;
     animation_count = 0;
  }

}
