package ar.edu.itba.ss;

import java.io.FileReader;
import java.nio.file.Paths;

import com.google.gson.Gson;

public class CoupledOscillator {
    private String configPath = "../config.json";
    private final static String rootDir = System.getProperty("user.dir");

    private static Config config;

    public void setUp() {

        configPath = Paths.get(rootDir, configPath).toString();
        try (FileReader reader = new FileReader(configPath)) {
            config = new Gson().fromJson(reader, Config.class);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public CoupledOscillator() {

    }

    public void run() {

    }

    public static void main(String[] args) {
        CoupledOscillator app = new CoupledOscillator();
        app.setUp();
        System.out.println(config);
        app.run();

    }
}
