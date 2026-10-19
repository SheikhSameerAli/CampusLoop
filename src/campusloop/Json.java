package campusloop;
import java.util.*;
/** Small output-only JSON encoder; API input uses standard URL-encoded forms. */
public final class Json {
 public static String encode(Object o){
  if(o==null)return "null";if(o instanceof Number||o instanceof Boolean)return o.toString();
  if(o instanceof Map<?,?> m){var a=new ArrayList<String>();m.forEach((k,v)->a.add(encode(k.toString())+":"+encode(v)));return "{"+String.join(",",a)+"}";}
  if(o instanceof Iterable<?> it){var a=new ArrayList<String>();for(Object v:it)a.add(encode(v));return "["+String.join(",",a)+"]";}
  var b=new StringBuilder("\"");for(char c:o.toString().toCharArray()){switch(c){case '"'->b.append("\\\"");case '\\'->b.append("\\\\");case '\n'->b.append("\\n");case '\r'->b.append("\\r");case '\t'->b.append("\\t");default->{if(c<32)b.append(String.format("\\u%04x",(int)c));else b.append(c);}}}return b.append('"').toString();
 }
 public static Map<String,Object> obj(Object... xs){var m=new LinkedHashMap<String,Object>();for(int i=0;i<xs.length;i+=2)m.put((String)xs[i],xs[i+1]);return m;}
}
