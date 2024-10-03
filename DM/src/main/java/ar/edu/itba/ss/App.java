package ar.edu.itba.ss;

/**
 * Hello world!
 *
 */

import com.google.gson.Gson;
import java.nio.file.Paths;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

public class App {

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

    public void run() {
        Oscillator oscillator;
        switch (config.getMethod()) {
            case "Verlet":
                oscillator = new Verlet(config.getMass(), config.getK(), config.getGamma(), config.getR0(),
                        config.getV0(),
                        config.getA0(), config.getT0(), config.getDt());
                break;
            case "Beeman":
                oscillator = new Beeman(config.getMass(), config.getK(), config.getGamma(), config.getR0(),
                        config.getV0(),
                        config.getA0(), config.getT0(), config.getDt());
                break;
            case "Gear5":
                oscillator = new Gear5(config.getMass(), config.getK(), config.getGamma(), config.getR0(),
                        config.getV0(),
                        config.getA0(), config.getT0(), config.getDt());

                break;

            default:
                throw new RuntimeException("Unknown method: " + config.getMethod());

        }

        try (FileWriter writer = new FileWriter(config.getMethod() + "_output.csv")) {
            writer.write("t,r,v,a\n");
            for (int i = 0; i < config.getSteps(); i++) {
                oscillator.step();
                writer.write(oscillator.getT() + "," + oscillator.getR() + "," + oscillator.getV() + ","
                        + oscillator.getA() + "\n");
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

    }

    public static void main(String[] args) {
        App app = new App();
        app.setUp();
        System.out.println(config);
        app.run();
    }
}
