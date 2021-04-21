'''
Litt usikker på om jeg må importere ting til modul når all koden uansett blir kjørt fra annet script ..
dette handler om namespace.. hvor er det funksjon søker over... der den blir definert eller den blir kjørt. hmhm.
'''
import numpy as np
import matplotlib.pyplot as plt
import panel as pn; pn.extension()
from scipy import stats
from scipy.integrate import quad
# utilities
def get_critical_values(test_dist_hyp, α, μ_true, μ_hyp, two_sided):

    if not two_sided:
        if μ_true >= μ_hyp:
            t_lower = -100 # kunne i praksis hvert -np.inf
            t_upper = test_dist_hyp.ppf(1-α)
        elif μ_true < μ_hyp:
            t_lower = test_dist_hyp.ppf(α)
            t_upper = 100
    else:
        t_lower = test_dist_hyp.ppf(α/2)
        t_upper = test_dist_hyp.ppf(1-α/2)
    return t_lower, t_upper

def power(dist, t_lower, t_upper):
        return 1-quad(dist, t_lower, t_upper)[0]
    
def make_power_grid(μ_hyp, σ_true, N,  t_lower, t_upper):
    μ_grid = np.linspace(-1,1, 40) # lavt antall gir raskere program .. 
    
    power_grid = np.empty(len(μ_grid))
    for i in range(len(μ_grid)):
        dist = stats.norm(loc=(μ_grid[i]-μ_hyp)/(σ_true/np.sqrt(N)), scale=1).pdf
        power_grid[i] = power(dist, t_lower, t_upper)
    return μ_grid, power_grid

def make_power_val(μ_hyp, μ_true, σ_true, N,  t_lower, t_upper):
    dist = stats.norm(loc=(μ_true-μ_hyp)/(σ_true/np.sqrt(N)), scale=1).pdf
    power_val = power(dist, t_lower, t_upper)
    return power_val

# plot functions
def make_plot0(test_dist_true, test_dist_hyp, t_lower, t_upper, two_sided, ax):
    
    grid = np.linspace(-3.5,3.5, num=200)
    ax.plot(grid, test_dist_hyp.pdf(grid), linewidth=2, label='nullhypotese')
    ax.plot(grid, test_dist_true.pdf(grid), linewidth=2, label=r'sann $\mu$')
    ax.hlines(0, t_lower, t_upper, color='black')
    ax.vlines(t_lower, -0.01, 0.01, color='black')
    ax.vlines(t_upper, -0.01, 0.01, color='black')
    if two_sided:
        t_grid = np.linspace(t_lower, t_upper)
    else:
        if t_lower < -3: # veldig hacky
            t_grid = np.linspace(-4, t_upper)
        else:
            t_grid = np.linspace(t_lower, 4)
    ax.fill_between(t_grid,0, test_dist_true.pdf(t_grid),
                    color='tab:orange', alpha=.5)
    
    ax.set(xlim=(-3.55, 3.55), ylim=(-0.01,0.65), xlabel='Verdi til testobservator',
           xticks=np.arange(-3, 3+1))
    ax.legend(title=r'Fordeling der $\mu$ tilsvarer',
              framealpha=0)
    ax.title.set_text('Fordeling til testobservatorer')                
    return ax
    
def make_plot1(μ_hyp, μ_true,σ_true, N,  t_lower, t_upper,α, ax):
    μ_grid, power_grid = make_power_grid(μ_hyp, σ_true, N,  t_lower, t_upper)
    power_val = make_power_val(μ_hyp, μ_true, σ_true, N,  t_lower, t_upper)
    
    ax.plot(μ_grid, power_grid, color='black')
    ax.scatter(μ_true, power_val, color='tab:orange', s=100)
    ax.set(xlim=(-1.05, 1.05), ylim = (-.01, 1.05), xlabel=r'Sann forventningsverdi', ylabel='Styrke',
          xticks=[-1, -0.5, 0, 0.5, 1])
    ax.title.set_text(r'Styrke, 1-P(type-II feil), som funksjon av sann $\mu$')
    return ax
    
def make_plot(μ_true, σ_true, μ_hyp, N, α, two_sided):
    if two_sided == 'Tosidig':
        two_sided = True
    else:
        two_sided = False

    test_dist_hyp = stats.norm(loc=0, scale=1)
    test_dist_true = stats.norm(loc=(μ_true-μ_hyp)/(σ_true/np.sqrt(N)), scale=1)
    t_lower, t_upper = get_critical_values(test_dist_hyp, α, μ_true, μ_hyp, two_sided)
    
    fig, axes = plt.subplots(1,2, figsize=(14,6))
    axes[0] = make_plot0(test_dist_true, test_dist_hyp, t_lower, t_upper, two_sided, axes[0])
    axes[1] = make_plot1(μ_hyp, μ_true,σ_true, N, t_lower, t_upper, α, axes[1])
    plt.close(fig)
    return fig