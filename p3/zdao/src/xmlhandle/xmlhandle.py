#coding=utf-8 
#!/usr/bin/python 
#<?xml version="1.0"?> 
#<data> 
#  <country name="Singapore"> 
#    <rank>4</rank> 
#    <year>2011</year> 
#    <gdppc>59900</gdppc> 
#    <neighbor name="Malaysia" direction="N"/> 
#  </country> 
#  <country name="Panama"> 
#    <rank>68</rank> 
#    <year>2011</year> 
#    <gdppc>13600</gdppc> 
#    <neighbor name="Costa Rica" direction="W"/> 
#    <neighbor name="Colombia" direction="E"/> 
#  </country> 
#</data>   
import xml.sax 
  
class CountryHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.asrname= ""
        self.asrresult=""
    
    def startElement(self,tag,attributes):
        if tag == "audio"
            
    # 元素开始事件处理 
    def startElement(self, tag, attributes): 
   self.CurrentData = tag 
   if tag == "country": 
     print "*****Country*****"
     name = attributes["name"] 
     print "name:", name 
   elif tag == "neighbor": 
     name = attributes["name"] 
     direction = attributes["direction"] 
     print name, "->", direction 
  
  # 元素结束事件处理 
  def endElement(self, tag): 
   if self.CurrentData == "rank": 
     print "rank:", self.rank 
   elif self.CurrentData == "year": 
     print "year:", self.year 
   elif self.CurrentData == "gdppc": 
     print "gdppc:", self.gdppc 
   self.CurrentData = "" 
  
  # 内容事件处理 
  def characters(self, content): 
   if self.CurrentData == "rank": 
     self.rank = content 
   elif self.CurrentData == "year": 
     self.year = content 
   elif self.CurrentData == "gdppc": 
     self.gdppc = content 
   
if __name__ == "__main__": 
   # 创建一个 XMLReader 
  parser = xml.sax.make_parser() 
  # turn off namepsaces 
  parser.setFeature(xml.sax.handler.feature_namespaces, 0) 
  
   # 重写 ContextHandler 
  Handler = CountryHandler() 
  parser.setContentHandler(Handler) 
    
  parser.parse("country.xml") 