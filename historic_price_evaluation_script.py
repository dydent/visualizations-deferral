# local imports

from helpers.historic_evaluation_helpers.create_historic_plots import plot_historic_network_data, \
    plot_historic_network_data_gas_cost, plot_historic_network_data_fiat_cost
from helpers.historic_evaluation_helpers.fetch_historic_gas_prices import fetch_historic_gas_prices

# ---------------------------------------------------------------------------------
# ANALYSIS SCRIPT FOR HISTORIC GAS PRICE EVALUATION
# ---------------------------------------------------------------------------------
from helpers.save_helpers.save_visualizations import save_visualization_figure

# e.g. the gas used value that is used to calculate the gas and fiat costs
# avg gas used per transaction in evaluation run with 500 users for V2ReferralMultilevelRewardsUpgradable contract
gas_used_baseline_value = 103211

# define the networks for which the historic data should be fetched
networks = ["eth", "bsc", "arb", "avax", "poly", "opt"]

# define the metric that should be used
historic_metric_type = "low"

# fetch data
historic_gas_price_data = fetch_historic_gas_prices(networks=networks)

# ---------------------------------------------------------------------------------
# HISTORIC GAS PRICES
# ---------------------------------------------------------------------------------
gas_prices_figure_title = f"Gas Prices ({historic_metric_type.title()}) in Gwei per Chains per Day Over Time"
gas_prices_figure_name = f"historic_{historic_metric_type}_gas_prices_over_time"
gas_prices_figure = plot_historic_network_data(historic_gas_price_data,
                                               title=gas_prices_figure_title,
                                               y_axis_title=f"Gas Price ({historic_metric_type.title()}) "
                                                            f"in Gwei",
                                               metric="gasPrice", metric_type=historic_metric_type)
save_visualization_figure(fig=gas_prices_figure,
                          file_name=gas_prices_figure_name,
                          base_folder="historical/gas-prices",
                          file_folder="")

# ---------------------------------------------------------------------------------
# HISTORIC TOKEN / FIAT PRICES (IN USD)
# ---------------------------------------------------------------------------------
token_prices_figure_title = f"Cryptocurrency Prices ({historic_metric_type.title()}) in USD per Chains per Day Over Time"
token_prices_figure_name = f"historic_{historic_metric_type}_token_currency_prices_over_time"
token_prices_figure = plot_historic_network_data(historic_gas_price_data,
                                                 title=token_prices_figure_title,
                                                 y_axis_title=f"Cryptocurrency Price ({historic_metric_type.title()}) in USD",
                                                 metric="tokenPrice", metric_type=historic_metric_type)
save_visualization_figure(fig=token_prices_figure,
                          file_name=token_prices_figure_name,
                          base_folder="historical/cryptocurrency-prices",
                          file_folder="")

# ---------------------------------------------------------------------------------
# HISTORIC GAS COSTS with custom gas used baseline from results
# ---------------------------------------------------------------------------------
gas_costs_figure_title = f"Gas Costs ({historic_metric_type.title()}) in Gwei per Chains per Day Over Time"
gas_cost_figure_name = f"historic_{historic_metric_type}_gas_costs_over_time"

gas_cost_figure = plot_historic_network_data_gas_cost(historic_gas_price_data,
                                                      y_axis_title=f"Gas Costs ({historic_metric_type.title()}) in Gwei",
                                                      metric_type=historic_metric_type,
                                                      gas_used_baseline=gas_used_baseline_value)
save_visualization_figure(fig=gas_cost_figure,
                          file_name=gas_cost_figure_name,
                          base_folder="historical/gas-costs",
                          file_folder="")

# ---------------------------------------------------------------------------------
# HISTORIC FIAT COSTS with custom gas used baseline from results in USD
# ---------------------------------------------------------------------------------
fiat_costs_figure_title = f"Fiat Costs ({historic_metric_type.title()}) in USD per Chains per Day Over Time"
fiat_cost_figure_name = f"historic_{historic_metric_type}_fiat_costs_over_time"

fiat_cost_figure = plot_historic_network_data_fiat_cost(historic_gas_price_data,
                                                        y_axis_title="Costs (USD)",
                                                        metric_type=historic_metric_type,
                                                        gas_used_baseline=gas_used_baseline_value)
save_visualization_figure(fig=fiat_cost_figure,
                          file_name=fiat_cost_figure_name,
                          base_folder="historical/fiat-costs",
                          file_folder="")
