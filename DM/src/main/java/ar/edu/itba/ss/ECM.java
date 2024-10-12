package ar.edu.itba.ss;

import com.google.gson.Gson;
import java.nio.file.Paths;
import java.io.FileReader;
import java.io.FileWriter;

public class ECM {

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
        config.setV0(-config.getGamma() / (2 * config.getMass()));

        config.setA0((-config.getK() * config.getR0() - config.getGamma() * config.getV0()) / config.getMass());
    }

    public double analyticalSolution(double t) {
        return Math.exp(-config.getGamma() * t / (2 * config.getMass())) * Math.cos(Math.sqrt(
                config.getK() / config.getMass() - Math.pow(config.getGamma(), 2) / (4 * Math.pow(config.getMass(), 2)))
                * t);
    }

    public void run() {
        Oscillator verlet = new Verlet(config.getMass(), config.getK(), config.getGamma(), config.getR0(),
                config.getV0(),
                config.getA0(), config.getT0(), config.getDt());
        Oscillator beeman = new Beeman(config.getMass(), config.getK(), config.getGamma(), config.getR0(),
                config.getV0(),
                config.getA0(), config.getT0(), config.getDt());
        Oscillator gear5 = new Gear5(config.getMass(), config.getK(), config.getGamma(), config.getR0(),
                config.getV0(),
                config.getA0(), config.getT0(), config.getDt());

        try (FileWriter writer = new FileWriter("ecm_dt_" + config.getDt() + ".csv")) {
            writer.write("v,b,g\n");
            for (int i = 0; i < config.getSteps(); i++) {
                verlet.step();
                beeman.step();
                gear5.step();
                writer.write(Math.pow(verlet.getR() - analyticalSolution(verlet.getT()), 2) + ","
                        + Math.pow(beeman.getR() - analyticalSolution(beeman.getT()), 2) + ","
                        + Math.pow(gear5.getR() - analyticalSolution(gear5.getT()), 2) + "\n");
            }
        } catch (

        Exception e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        ECM app = new ECM();
        System.out.println("Starting ECM");
        app.setUp();
        System.out.println(config);
        app.run();
    }

}
