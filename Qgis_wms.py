#-*- coding: utf-8 -*-
from qgis.gui import QgsMapTool
import httplib 
from urllib import urlencode
import ast
import re
import sys


class PointTool(QgsMapTool):
  
  def __init__(self, canvas):
    QgsMapTool.__init__(self, canvas)
    self.canvas = canvas
    self.x=[]
    
  def canvasPressEvent(self, event):
     pass
     
  def canvasMoveEvent(self, event):
    x = event.pos().x()
    y = event.pos().y()
    point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
    
    
  def canvasReleaseEvent(self, event):
        #Get the click
    x = event.pos().x()
    y = event.pos().y()
    
    point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
    self.x.append(point[1])
    self.x.append(point[0])
    #print " x:%d - y:%d" % (point[1],point[0])
    #print self.x
    return self.x
    
  def activate(self):
    pass
    
  def deactivate(self):
    pass
    
  def isZoomTool(self):
    return False
    
  def isTransient(self):
    return False
    
  def isEditTool(self):
    return True
    
    
if __name__ == "__main__":
  canvas=qgis.utils.iface.mapCanvas()
  tool = PointTool(canvas)
  canvas.setMapTool(tool)
  
  #вызов класса
  while len(tool.x)==0: 
    canvas.setMapTool(tool)
    print tool.x
  
  #x=6180490.0
  #y=3901390.0
  x=tool.x[0]
  y=tool.x[1]
  
  #print "1-",x
  #print "1-",y
  
  str_reqest=urlencode({'x':str(x),'y':str(y),'zoom':'14'})+"&actLayers%5B%5D=kadastr"
  headers = {
  "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
  "Accept": "application/json , text/javascript, */*; q=0.01",
  "Accept-Encoding":"gzip, deflate",  
  "Accept-Language": "en-US,en;q=0.8,ru;q=0.6",
  "Connection": "keep-alive",
  "X-Requested-With":"XMLHttpRequest",
  "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
  "Referer": "http://map.land.gov.ua/kadastrova-karta/getobjectinfo"}
  con=httplib.HTTPConnection('map.land.gov.ua')
  con.request("POST","/kadastrova-karta/getobjectinfo",str_reqest,headers=headers)
  result_data=con.getresponse().read()
  #Преобразование результата ответа сервера в словарь
  result_dict=ast.literal_eval(result_data)
  if result_dict.get('dilanka')<>None:
      str_dil=result_dict['dilanka']
      str_ikk=result_dict['ikk']
      str_rajon=result_dict['rajonunion']
      str_obl=result_dict['obl']
  
      reg_exp=re.compile(ur":<./div>(.*?)<",re.U|re.I)
      kad_num = re.compile(ur"[0-9]{10}:[0-9]{2}:[0-9]{3}:[0-9]{4}",re.U)
  
      s_all_dilanka=reg_exp.findall(str_dil)
      vlastn=s_all_dilanka[1]
      #print type(vlastn.decode("utf-8"))
      goal=s_all_dilanka[2]
      area=s_all_dilanka[3]
      s_kad_num=kad_num.findall(str_dil)[0]
  
      s_all_ikk=reg_exp.findall(str_ikk)
      district=s_all_ikk[0]
      koatuu=s_all_ikk[1]
      zone=s_all_ikk[2]
      kvartal=s_all_ikk[3]
      print "_____"
      print
      print u'Кадастровий номер: ',
      print s_kad_num.decode('unicode-escape')
      print u"Тип власностi: ", 
      print vlastn.decode('unicode-escape')
      print u"Цiльове призначення: ", 
      print goal.decode('unicode-escape')
      print u"Площа: ", 
      print area.decode('unicode-escape')
      print u"Район: ",
      print  district.decode('unicode-escape')
      print u"КОАТУУ: ", 
      print koatuu.decode('unicode-escape')
      print u"Зона: ", 
      print zone.decode('unicode-escape')
      print u"Квартал: ", 
      print kvartal.decode('unicode-escape')
  else:
    print 
    print u"У запит не потрапило жодної земельної дiлянки !"
  con.close()