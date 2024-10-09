package ar.edu.itba.ss;

import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
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

    public CoupledOscillator() {

    }

    public void run() {
            try (FileWriter writer = new FileWriter(config.getMethod() + "_output.csv")) {
            writer.write("t,r,v,a\n");
            Double prevY = 0.0;
            Double currentY = 0.0;
            Oscillator aux;
            for (int i = 0; i < config.getSteps(); i++) {
                for (int j = 0; j<oscillators.size();j++) {
                    aux = oscillators.get(j);
                    currentY = aux.getR();
                    if(j==0)
                        aux.firstStep(config.getA(),config.getOmega());
                    else if(j == oscillators.size()-1)
                        aux.lastStep();//cambiar por un break? nose
                    else{
                        aux.coupledStep(currentY,oscillators.get(j+1).getR());
                    }
                    prevY = currentY;
                    for (Oscillator toWrite : oscillators) {
                        writer.write(toWrite.getT() + "," + toWrite.getR() + "," + toWrite.getV() + ","
                            + toWrite.getA() + "\n");
                    }
            }
        }
        } catch (IOException e) {
            e.printStackTrace();
        }


    }

    public static void main(String[] args) {
        CoupledOscillator app = new CoupledOscillator();
        app.setUp();
        System.out.println(config);
        app.run();

    }
}
