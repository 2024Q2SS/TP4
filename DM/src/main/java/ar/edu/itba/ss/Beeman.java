package ar.edu.itba.ss;

public class Beeman extends Oscillator {

    private Double aPrev;

    public Beeman(Double m, Double k, Double gamma, Double r, Double v, Double a, Double t, Double dt) {
        super(m, k, gamma, r, v, a, t, dt);
    }

    @Override
    public Oscillator create(){
        return new Beeman(getM(), getK(), getGamma(), getR(), getV(), getA(), getT(), getDt());
    }
    
    @Override
    public void coupledStep(Double prevY, Double nextY){

    }

    @Override
    public void firstStep(){

    }
    
    @Override
    public void lastStep(){

    }
    public void initializeValues() {
        double vPrev = getV() + getDt() * getA();
        double rPrev = getR() + getDt() * vPrev + getDt() * getDt() * getA() / 2;
        aPrev = (-getK() * rPrev - getGamma() * vPrev) / getM();
    }

    public void step() {
        double rNext = getR() + getV() * getDt() + 2.0 / 3.0 * getA() * getDt() * getDt()
                - 1.0 / 6.0 * aPrev * getDt() * getDt();

        double vNext = getV() + 3.0 / 2.0 * getA() * getDt() - 1.0 / 2.0 * aPrev * getDt();
        double aNext = (-getK() * rNext - getGamma() * vNext) / getM();

        vNext = getV() + 1.0 / 3.0 * aNext * getDt() + 5.0 / 6.0 * getA() * getDt() - 1.0 / 6.0 * aPrev * getDt();

        aPrev = getA();

        setR(rNext);
        setV(vNext);
        setA(aNext);
        this.setT(this.getT() + this.getDt());
    }
}
