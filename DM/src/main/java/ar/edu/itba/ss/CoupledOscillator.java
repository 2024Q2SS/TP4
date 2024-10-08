package ar.edu.itba.ss;

import java.io.FileReader;
import java.nio.file.Paths;
import java.util.ArrayList;

import com.google.gson.Gson;

public class CoupledOscillator {
    private String configPath = "../config.json";
    private final static String rootDir = System.getProperty("user.dir");

    private static Config config;
    private ArrayList<Oscillator> oscillators;
    private Double acceleration;
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
        Oscillator creator;
        switch(config.getMethod()){
            case "Verlet":
                creator = new Verlet(config.getMass(), config.getK(), config.getGamma(), config.getR0(),
                        config.getV0(),
                        config.getA0(), config.getT0(), config.getDt());
                break;
            case "Beeman":
                creator = new Beeman(config.getMass(), config.getK(), config.getGamma(), config.getR0(),
                        config.getV0(),
                        config.getA0(), config.getT0(), config.getDt());
                break;
            case "Gear5":
                creator = new Gear5(config.getMass(), config.getK(), config.getGamma(), config.getR0(),
                        config.getV0(),
                        config.getA0(), config.getT0(), config.getDt());

                break;

            default:
                throw new RuntimeException("Unknown method: " + config.getMethod());

 
        }
        for (int i = 0; i < config.getN(); i++) {
            oscillators.add(creator.create());
        }


    }

    public static void main(String[] args) {
        CoupledOscillator app = new CoupledOscillator();
        app.setUp();
        System.out.println(config);
        app.run();

    }
}
