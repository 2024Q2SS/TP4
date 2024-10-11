package ar.edu.itba.ss;

public class Verlet extends Oscillator implements IntegrationMethod {

    private Double rPrev;

    public Verlet(Double m, Double k, Double gamma, Double r, Double v, Double a, Double t, Double dt) {
        super(m, k, gamma, r, v, a, t, dt);

    }

    @Override
    public Oscillator create() {
        return new Verlet(getM(), getK(), getGamma(), getR(), getV(), getA(), getT(), getDt());
    }

    @Override
    public void coupledStep(Double prevY, Double nextY) {
        double force = (-getK() * (getR() - prevY) - getK() * (getR() - nextY));

        double newA = force / getM();

        double rNext = 2 * getR() - rPrev + (newA * getDt() * getDt());

        double newV = (rNext - rPrev) / (2 * getDt());

        rPrev = getR();

        setA(newA);
        setV(newV);
        setR(rNext);
        this.setT(this.getT() + this.getDt());
    }

    @Override
    public void firstStep(Double A, Double omega) {
        setR(A * Math.sin(omega * getT()));
        this.setT(this.getT() + this.getDt());
    }

    @Override
    public void lastStep() {
        this.setT(this.getT() + this.getDt());
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
