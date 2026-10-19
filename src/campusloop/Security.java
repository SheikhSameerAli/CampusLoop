package campusloop;
import java.security.*;import java.util.*;import javax.crypto.SecretKeyFactory;import javax.crypto.spec.PBEKeySpec;
public final class Security {
 private static final SecureRandom RANDOM=new SecureRandom();
 public static String token(){byte[] b=new byte[32];RANDOM.nextBytes(b);return Base64.getUrlEncoder().withoutPadding().encodeToString(b);}
 public static String password(String p){byte[] salt=new byte[16];RANDOM.nextBytes(salt);return "210000:"+Base64.getEncoder().encodeToString(salt)+":"+Base64.getEncoder().encodeToString(derive(p,salt,210000));}
 private static byte[] derive(String p,byte[] salt,int iterations){var spec=new PBEKeySpec(p.toCharArray(),salt,iterations,256);try{return SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256").generateSecret(spec).getEncoded();}catch(Exception e){throw new IllegalStateException(e);}finally{spec.clearPassword();}}
 public static boolean verify(String p,String stored){try{String[] s=stored.split(":");return MessageDigest.isEqual(derive(p,Base64.getDecoder().decode(s[1]),Integer.parseInt(s[0])),Base64.getDecoder().decode(s[2]));}catch(Exception e){return false;}}
}
