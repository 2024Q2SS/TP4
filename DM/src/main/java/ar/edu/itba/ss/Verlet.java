package ar.edu.itba.ss;

public class Verlet extends Oscillator implements IntegrationMethod {

    private Double rPrev;

    public Verlet(Double m, Double k, Double gamma, Double r, Double v, Double a, Double t, Double dt) {
        super(m, k, gamma, r, v, a, t, dt);

    }

    public void initializeValues() {
        Double vPrev = getV() - getDt() * getA();
        rPrev = getR() - getDt() * vPrev + getDt() * getDt() * getA() / 2;
    }

    public void step() {
        double rNext = 2 * getR() - rPrev + getDt() * getDt() * getA();
        double vCurr = (rNext - rPrev) / (2 * getDt());

        rPrev = getR();

        setR(rNext);
        setV(vCurr);

        setA((-getK() * getR() - getGamma() * getV()) / getM());

        this.setT(this.getT() + this.getDt());

    }

}
