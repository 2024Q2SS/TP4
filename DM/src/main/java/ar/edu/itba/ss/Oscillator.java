package ar.edu.itba.ss;

public abstract class Oscillator {
    private Double y;
    private Double oldY;

    private Double m;
    private Double k;
    private Double gamma;

    private Double r;
    private Double v;
    private Double a;

    private Double t;
    private Double dt;

    public Oscillator(Double m, Double k, Double gamma, Double r, Double v, Double a, Double t, Double dt) {
        this.m = m;
        this.k = k;
        this.gamma = gamma;
        this.r = r;
        this.v = v;
        this.a = a;
        this.t = t;
        this.dt = dt;
        this.y = 0.0;

        initializeValues();
    }

    public abstract Oscillator create();
    
    public abstract void coupledStep(Double prevY, Double nextY);

    public abstract void firstStep(Double A, Integer omega);

    public abstract void lastStep();

    public Double getM() {
        return m;
    }

    public void setM(Double m) {
        this.m = m;
    }

    public Double getK() {
        return k;
    }

    public void setK(Double k) {
        this.k = k;
    }

    public Double getGamma() {
        return gamma;
    }

    public void setGamma(Double gamma) {
        this.gamma = gamma;
    }

    public Double getR() {
        return r;
    }

    public void setR(Double r) {
        this.r = r;
    }

    public Double getV() {
        return v;
    }

    public void setV(Double v) {
        this.v = v;
    }

    public Double getA() {
        return a;
    }

    public void setA(Double a) {
        this.a = a;
    }

    public Double getT() {
        return t;
    }

    public void setT(Double t) {
        this.t = t;
    }

    public Double getDt() {
        return dt;
    }

    public void setDt(Double dt) {
        this.dt = dt;
    }

    public abstract void step();

    public abstract void initializeValues();

	public Double getY() {
		return y;
	}

	public void setY(Double y) {
		this.y = y;
	}
}
