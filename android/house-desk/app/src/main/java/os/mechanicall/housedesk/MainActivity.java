package os.mechanicall.housedesk;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;

/**
 * Thin Leanback-friendly shell: loads myarch desk URL.
 * Authority and keys stay on the operator host — this is a view only.
 */
public class MainActivity extends Activity {
    private static final String FALLBACK_URL = "http://192.168.1.241:8788/";
    private static final String BRIDGE_PATH = "/sdcard/Mechanicall/bridge.url";

    private WebView web;

    @SuppressLint("SetJavaScriptEnabled")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        web = findViewById(R.id.webview);
        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setMediaPlaybackRequiresUserGesture(false);
        web.setWebViewClient(new WebViewClient());
        String url = readBridgeUrl();
        Toast.makeText(this, "Desk · propose only", Toast.LENGTH_SHORT).show();
        web.loadUrl(url);
    }

    private String readBridgeUrl() {
        File f = new File(BRIDGE_PATH);
        if (!f.isFile()) {
            return FALLBACK_URL;
        }
        try (BufferedReader br = new BufferedReader(new FileReader(f))) {
            String line = br.readLine();
            if (line != null) {
                line = line.trim();
                if (line.startsWith("http://") || line.startsWith("https://")) {
                    if (!line.endsWith("/")) {
                        line = line + "/";
                    }
                    return line;
                }
            }
        } catch (IOException ignored) {
        }
        return FALLBACK_URL;
    }

    @Override
    public void onBackPressed() {
        if (web != null && web.canGoBack()) {
            web.goBack();
        } else {
            super.onBackPressed();
        }
    }
}
