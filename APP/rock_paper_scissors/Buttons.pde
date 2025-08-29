class Button
{
  float posx1 = 0;
  float posy1 = 0;
  float posx2 = 0;
  float posy2 = 0;
  
  Button(float x1, float y1, float widthx, float heighty, String Text, float Textsize){
    
    
    posx1 = x1;
    posy1 = y1;
    posx2 = posx1 + widthx;
    posy2 = posy1 + heighty;
    
    //strokeWeight(1);
    //noStroke();
    
    //rectMode(CORNER);
    //rect(posx1, posy1, widthx, heighty);
    //rectMode(CENTER);
  
  
    textAlign(CENTER);
    textSize(Textsize);
    fill(0,0,0);
    float textx, texty;
    textx = posx1+((widthx/2));
    texty = (posy1+((heighty/2)))+(Textsize/4);
    if((mouseX > x1) && (mouseX < x1 + widthx) && (mouseY > y1) && (mouseY < y1 + heighty)){
       fill(255,0,0); 
    }
    text(Text, textx, texty);
    fill(255,255,255);

    
  }
  

  boolean Click(){
   boolean a = false;
   if(mousePressed == true){
      if( (mouseX >= posx1) && (mouseX <= posx2) && (mouseY >= posy1) && (mouseY <= posy2) ){
        a = true;
      }else{
        a = false;
      }
   }

    return a;
  }
  
  
  
}
