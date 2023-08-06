
from SBbadger import generate
from SBbadger import generate_serial

from scipy.special import zeta


# def in_dist(k):
#     return k ** (-2) / zeta(2)
#
#
# def out_dist(k):
#     return k ** (-2) / zeta(2)

def in_dist(k):
    return 159.56679886918792*k**(-1.6914416803009278)

def out_dist(k):
    return 152.91017262603404*k**(-1.2471437815467692)


if __name__ == "__main__":

    generate.models(
        group_name='mass_action',
        n_models=10,
        n_species=10,
        out_dist=out_dist,
        in_dist=in_dist,
        add_enzyme=True,
        rxn_prob=[.35, .30, .30, .05],
        kinetics=['mass_action', ['loguniform', 'loguniform', 'loguniform'],
                  ['kf', 'kr', 'kc'],
                  [[0.01, 100], [0.01, 100], [0.01, 100]]],
        allo_reg=[[0.5, 0.5, 0, 0], 0.5, ['uniform', 'uniform', 'uniform'],
                  ['ro', 'kma', 'ma'],
                  [[0, 1], [0, 1], [0, 1]]],
        overwrite=True,
        constants=True,
        source=[1, 'loguniform', 0.01, 1, 1],
        sink=[2, 'loguniform', 0.01, 1],
        rev_prob=1,
        ic_params=['uniform', 0, 10],
        net_plots=True,
        cobra=True
    )

    # generate.models(
    #
    #     group_name='mass_action',
    #     n_models=10,
    #     n_species=10,
    #     rxn_prob=[.35, .30, .30, .05],
    #     out_dist=out_dist,
    #     in_dist=in_dist,
    #     # rxn_prob=[1, .0, .0, .0],
    #     kinetics=['mass_action', ['loguniform', 'loguniform', 'loguniform'],
    #                              ['kf', 'kr', 'kc'],
    #                              [[0.01, 100], [0.01, 100], [0.01, 100]]],
    #     allo_reg=[[0.5, 0.5, 0, 0], 0.5, ['uniform', 'uniform', 'uniform'],
    #                                      ['ro', 'kma', 'ma'],
    #                                      [[0, 1], [0, 1], [0, 1]]],
    #     # allo_reg=True,
    #     add_enzyme=True,
    #     overwrite=True,
    #     source=[1, 'loguniform', 0.01, 1, 0.5],
    #     sink=[2, 'loguniform', 0.01, 1],
    #     # constants=False,
    #     constants=True,
    #     cobra=True,
    #     rev_prob=1,
    #     ic_params=['uniform', 0, 10],
    #     # dist_plots=True,
    #     net_plots=True
    #
    # )
