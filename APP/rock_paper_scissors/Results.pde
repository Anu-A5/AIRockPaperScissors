class Results
{
  
  int animation_int_time;
  int animation_gran;
  int animation_count = 0;
  
  Results()
  {
    animation_int_time = millis();
    animation_gran = 1000;
    animation_count = 0;
  }
  
  void draw()
  {
    int stroke = 50;
    
    int animation_x = width*1/6;
    int animation_y = height/2;
    int animation_w = (width*3/12);
    int animation_h = animation_w;
    int count_down_length = 3;    
    

    rectMode(CENTER);
    noStroke();
    
    if(CHEAT)
    {
      if(User_Throw.charAt(1)-48 == 1)//rock 
      {
         Comp_Throw = "22";
      }
      else if(User_Throw.charAt(1)-48 == 2)//rock vs scissors
      {
         Comp_Throw = "23";
      }
      else if(User_Throw.charAt(1)-48 == 3)//paper vs rock
      {
         Comp_Throw = "21";
      }
    }
    
    //draw computer
    fill(255,0,0);
    rect(animation_x, animation_y, animation_w+stroke, animation_w+stroke);
    switch(Comp_Throw.charAt(1)-48)
    {
       case(1):
         shape(Rock, animation_x - animation_w/2, animation_y-animation_h/2, animation_w, animation_h);
         break;
       case(2):
         shape(Paper, animation_x - animation_w/2, animation_y-animation_h/2, animation_w, animation_h);
         break;
       case(3):
         image(Scissors, animation_x - animation_w/2, animation_y-animation_h/2, animation_w, animation_h);
         break;
    } 
    
    
    
    //draw User
    fill(0,0,255);
    rect(animation_x*5, animation_y, animation_w+stroke, animation_w+stroke);
    switch(User_Throw.charAt(1)-48)
    {
       case(1):
         shape(Rock, animation_x*5 - animation_w/2, animation_y-animation_h/2, animation_w, animation_h);
         break;
       case(2):
         shape(Paper, animation_x*5 - animation_w/2, animation_y-animation_h/2, animation_w, animation_h);
         break;
       case(3):
         image(Scissors, animation_x*5 - animation_w/2, animation_y-animation_h/2, animation_w, animation_h);
         break;
    }
    
    
     //Do rock paper scissor animation.
    if(millis() > animation_int_time + animation_gran)
    {
       animation_int_time = millis();
       animation_gran     = 1000;
       animation_count++;
    }
    
    textSize(100);
    fill(255,142,97);
    text(count_down_length-animation_count, width*5/6, height*1/6);
   
  
    if((User_Throw.charAt(1)-48) == (Comp_Throw.charAt(1)-48))
    {
       fill(0,0,0);
       textAlign(CENTER);
       text("DRAW", width/2, height/2);
    }
    else if((User_Throw.charAt(1)-48 == 1) && (Comp_Throw.charAt(1)-48 == 2))//rock vs paper
    {
       fill(255,0,0);
       textAlign(CENTER);
       text("LOSE", width/2, height/2);
    }
    else if((User_Throw.charAt(1)-48 == 1) && (Comp_Throw.charAt(1)-48 == 3))//rock vs scissors
    {
       fill(0,255,0);
       textAlign(CENTER);
       text("WIN", width/2, height/2);
    }
    else if((User_Throw.charAt(1)-48 == 2) && (Comp_Throw.charAt(1)-48 == 3))//paper vs scissors
    {
       fill(255,0,0);
       textAlign(CENTER);
       text("LOSE", width/2, height/2);
    }
    else if((User_Throw.charAt(1)-48 == 2) && (Comp_Throw.charAt(1)-48 == 1))//paper vs rock
    {
       fill(0,255,0);
       textAlign(CENTER);
       text("WIN", width/2, height/2);
    }
    else if((User_Throw.charAt(1)-48 == 3) && (Comp_Throw.charAt(1)-48 == 2))//scissors vs paper
    {
       fill(0,255,0);
       textAlign(CENTER);
       text("WIN", width/2, height/2);
    }
    else if((User_Throw.charAt(1)-48 == 3) && (Comp_Throw.charAt(1)-48 == 1))//scissors vs rock
    {
       fill(255,0,0);
       textAlign(CENTER);
       text("LOSE", width/2, height/2);
    }else{
       fill(0,0,0);
       textAlign(CENTER);
       text("DRAW", width/2, height/2);
    }
    
    if((count_down_length-animation_count)==0){
      reset();
      run_game.reset();
      Current_Screen=1;
    }
  }
  
  void reset()
  {
     animation_int_time = millis();
     animation_gran = 1000;
     animation_count = 0;
  }
}
