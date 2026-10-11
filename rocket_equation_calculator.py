"""
Rocket Equation Calculator (Tsiolkovsky)
Basic educational project - Mechanical Engineering

delta_v = Isp * g0 * ln(m0 / mf)
  Isp : specific impulse (seconds)
  g0  : standard gravity = 9.81 m/s^2
  m0  : starting mass (fuel + rocket)
  mf  : final mass after fuel is burnt (dry mass)
"""
import math
import matplotlib.pyplot as plt

G0 = 9.81            # m/s^2
LEO_DELTA_V = 9400   # m/s, approx. needed to reach low Earth orbit (incl. losses)


def delta_v(isp, m0, mf):
    """Ideal delta-v of one stage in m/s."""
    return isp * G0 * math.log(m0 / mf)


def single_stage(isp, m0, mf):
    """Return delta-v, mass ratio and propellant fraction."""
    dv = delta_v(isp, m0, mf)
    mass_ratio = m0 / mf
    prop_fraction = (m0 - mf) / m0
    return dv, mass_ratio, prop_fraction


def two_stage(isp1, m0_1, mf_1, isp2, m0_2, mf_2):
    """Total delta-v of two stages. Stage 1 is dropped after burnout,
    so stage 2 starts with its own mass (m0_2)."""
    return delta_v(isp1, m0_1, mf_1) + delta_v(isp2, m0_2, mf_2)


def plot_dv_vs_mass_ratio(isp):
    """Graph of delta-v against mass ratio for the given Isp."""
    ratios = [1 + 0.1 * i for i in range(0, 120)]   # 1.0 to ~12.9
    dvs = [isp * G0 * math.log(r) / 1000 for r in ratios]   # km/s
    plt.figure(figsize=(7, 4.5))
    plt.plot(ratios, dvs, label=f"Isp = {isp} s")
    plt.axhline(LEO_DELTA_V / 1000, color="red", linestyle="--",
                label="Approx. LEO requirement (9.4 km/s)")
    plt.xlabel("Mass ratio (m0 / mf)")
    plt.ylabel("Delta-v (km/s)")
    plt.title("Delta-v vs Mass Ratio")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("delta_v_vs_mass_ratio.png", dpi=150)
    print("Graph saved as delta_v_vs_mass_ratio.png")


def ask(prompt):
    return float(input(prompt))


def main():
    print("=== ROCKET EQUATION CALCULATOR ===")
    print("1. Single stage")
    print("2. Two stage")
    choice = input("Choose 1 or 2: ").strip()

    if choice == "1":
        isp = ask("Specific impulse Isp (s): ")
        m0 = ask("Starting mass m0 (kg): ")
        mf = ask("Dry mass mf (kg): ")
        if mf <= 0 or m0 <= mf:
            print("Error: need m0 > mf > 0.")
            return
        dv, mr, pf = single_stage(isp, m0, mf)
        print(f"\nDelta-v           : {dv:.1f} m/s ({dv/1000:.2f} km/s)")
        print(f"Mass ratio        : {mr:.2f}")
        print(f"Propellant fraction: {pf*100:.1f} %")
        print(f"Compared with LEO : {dv/LEO_DELTA_V*100:.1f} % of 9.4 km/s")
        if dv >= LEO_DELTA_V:
            print("This could reach low Earth orbit (ideal case).")
        else:
            print("Not enough to reach low Earth orbit.")
        plot_dv_vs_mass_ratio(isp)

    elif choice == "2":
        print("--- Stage 1 ---")
        isp1 = ask("Isp (s): ")
        m0_1 = ask("Starting mass of whole rocket (kg): ")
        mf_1 = ask("Mass after stage 1 fuel burnt, before dropping stage (kg): ")
        print("--- Stage 2 ---")
        isp2 = ask("Isp (s): ")
        m0_2 = ask("Starting mass of stage 2 (kg): ")
        mf_2 = ask("Final dry mass of stage 2 (kg): ")
        total = two_stage(isp1, m0_1, mf_1, isp2, m0_2, mf_2)
        print(f"\nTotal delta-v     : {total:.1f} m/s ({total/1000:.2f} km/s)")
        print(f"Compared with LEO : {total/LEO_DELTA_V*100:.1f} % of 9.4 km/s")
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()
