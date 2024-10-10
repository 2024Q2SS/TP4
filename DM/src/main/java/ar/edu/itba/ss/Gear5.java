package ar.edu.itba.ss;

/**
 * Gear5
 */
public class Gear5 extends Oscillator implements IntegrationMethod {
    private Double r3;
    private Double r4;
    private Double r5;

    private Double rPred;
    private Double vPred;

    public Gear5(Double m, Double k, Double gamma, Double r, Double v, Double a, Double t, Double dt) {
        super(m, k, gamma, r, v, a, t, dt);
    }

    @Override
    public Oscillator create() {
        return new Gear5(getM(), getK(), getGamma(), getR(), getV(), getA(), getT(), getDt());
    }

    @Override
    public void coupledStep(Double prevY, Double nextY) {

    }

    @Override
    public void initializeValues() {
        this.r3 = (-getK() * getV() - getGamma() * getA()) / getM();
        this.r4 = (-getK() * getA() - getGamma() * r3) / getM();
        this.r5 = (-getK() * r3 - getGamma() * r4) / getM();
    }

    public void step() {
        double factor2 = Math.pow(getDt(), 2) / 2;
        double factor3 = Math.pow(getDt(), 3) / 6;
        double factor4 = Math.pow(getDt(), 4) / 24;
        double factor5 = Math.pow(getDt(), 5) / 120;

        // Calculating predictions
        rPred = getR() + getDt() * getV() + factor2 * getA() + factor3 * r3 + factor4 * r4 + factor5 * r5;
        vPred = getV() + getDt() * getA() + factor2 * r3 + factor3 * r4 + factor4 * r5;
        double aPred = getA() + getDt() * r3 + factor2 * r4 + factor3 * r5;
        double r3Pred = r3 + getDt() * r4 + factor2 * r5;
        double r4Pred = r4 + getDt() * r5;
        double r5Pred = r5;

        // Evaluating acceleration
        double dR2 = ((calculate() - aPred) * Math.pow(getDt(), 2)) / 2;

        // Correcting predictions
        setR(rPred + 3.0 / 16 * dR2);
        setV(vPred + ((251.0 / 360) * dR2) / getDt());
        setA(aPred + dR2 / factor2);
        r3 = r3Pred + ((11.0 / 18) * dR2) / factor3;
        r4 = r4Pred + ((1.0 / 6) * dR2) / factor4;
        r5 = r5Pred + ((1.0 / 60) * dR2) / factor5;

        Double auxT = getT() + getDt();
        setT(auxT);
    }

    public Double calculate() {
        return (-getK() * rPred - getGamma() * vPred) / getM();
    }

    @Override
    public void firstStep(Double A, Integer omega) {
        setR(A * Math.sin(omega * getT()));
    }

    @Override
    public void lastStep() {

    }

}
