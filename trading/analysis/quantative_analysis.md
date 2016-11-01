
# Analysis of trading algorithm
DISCLAIMER: This analysis is done on a quite simple trading algorithm as our value investment algorithm is not yet finished. As a comparison benchmark for the algorithm we used the S&P500, which includes the shares of the 500 largest companies.

This notebook includes the analysis of the first part of our hypothesis. 

Our hypothesis:
A distributed autonomous hedge fund implemented in a blockchain based on smart contracts is (1) able to be more profitable than benchmark indexes and (2) investments follow sustainability criteria that are transparent to the investors.

## Load data into notebook
We are using [zipline](https://github.com/quantopian/zipline) to simulate our trading algorithms. Zipline offers to output the results of the simulation as a pandas pickle file. The advantage of using zipline is that it already calculates common indicators including sharpe, alpha, beta and the return.

We simulated our simple algorithm for a random period of two months. The period covered is from beginning of October 2013 to end of November 2013.



```python
import pandas as pd
performance = pd.read_pickle('results/momentum_pipeline.pickle')
# display the top 5 rows to see if the load worked
performance.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>algo_volatility</th>
      <th>algorithm_period_return</th>
      <th>alpha</th>
      <th>benchmark_period_return</th>
      <th>benchmark_volatility</th>
      <th>beta</th>
      <th>capital_used</th>
      <th>ending_cash</th>
      <th>ending_exposure</th>
      <th>ending_value</th>
      <th>...</th>
      <th>short_value</th>
      <th>shorts_count</th>
      <th>sortino</th>
      <th>starting_cash</th>
      <th>starting_exposure</th>
      <th>starting_value</th>
      <th>trading_days</th>
      <th>transactions</th>
      <th>treasury_period_return</th>
      <th>universe_size</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2013-10-07 20:00:00</th>
      <td>NaN</td>
      <td>0.000000</td>
      <td>NaN</td>
      <td>-0.008506</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.000000</td>
      <td>10000000.000000</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>...</td>
      <td>0.00</td>
      <td>0</td>
      <td>NaN</td>
      <td>10000000.000000</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>1</td>
      <td>[]</td>
      <td>0.0265</td>
      <td>3046</td>
    </tr>
    <tr>
      <th>2013-10-08 20:00:00</th>
      <td>0.000740</td>
      <td>-0.000066</td>
      <td>0.036942</td>
      <td>-0.020734</td>
      <td>0.042944</td>
      <td>0.017234</td>
      <td>164224.755949</td>
      <td>10164224.755949</td>
      <td>-164884.07</td>
      <td>-164884.07</td>
      <td>...</td>
      <td>-1111751.72</td>
      <td>2</td>
      <td>-11.224972</td>
      <td>10000000.000000</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>2</td>
      <td>[{'dt': 2013-10-08 20:00:00+00:00, 'commission...</td>
      <td>0.0266</td>
      <td>3046</td>
    </tr>
    <tr>
      <th>2013-10-09 20:00:00</th>
      <td>0.031015</td>
      <td>0.003284</td>
      <td>0.758649</td>
      <td>-0.020172</td>
      <td>0.105230</td>
      <td>0.283593</td>
      <td>-136252.190979</td>
      <td>10027972.564970</td>
      <td>4871.72</td>
      <td>4871.72</td>
      <td>...</td>
      <td>-2191421.49</td>
      <td>3</td>
      <td>456.600448</td>
      <td>10164224.755949</td>
      <td>-164884.07</td>
      <td>-164884.07</td>
      <td>3</td>
      <td>[{'dt': 2013-10-09 20:00:00+00:00, 'commission...</td>
      <td>0.0268</td>
      <td>3046</td>
    </tr>
    <tr>
      <th>2013-10-10 20:00:00</th>
      <td>0.051333</td>
      <td>-0.001261</td>
      <td>-0.065033</td>
      <td>0.001219</td>
      <td>0.242613</td>
      <td>-0.136551</td>
      <td>-753117.984898</td>
      <td>9274854.580071</td>
      <td>712533.34</td>
      <td>712533.34</td>
      <td>...</td>
      <td>-3758922.04</td>
      <td>4</td>
      <td>-2.182774</td>
      <td>10027972.564970</td>
      <td>4871.72</td>
      <td>4871.72</td>
      <td>4</td>
      <td>[{'dt': 2013-10-10 20:00:00+00:00, 'commission...</td>
      <td>0.0271</td>
      <td>3049</td>
    </tr>
    <tr>
      <th>2013-10-11 20:00:00</th>
      <td>0.068803</td>
      <td>-0.008960</td>
      <td>-0.380379</td>
      <td>0.007513</td>
      <td>0.214236</td>
      <td>-0.179221</td>
      <td>-1215165.423702</td>
      <td>8059689.156369</td>
      <td>1850712.22</td>
      <td>1850712.22</td>
      <td>...</td>
      <td>-4379532.24</td>
      <td>4</td>
      <td>-7.109571</td>
      <td>9274854.580071</td>
      <td>712533.34</td>
      <td>712533.34</td>
      <td>5</td>
      <td>[{'dt': 2013-10-11 20:00:00+00:00, 'commission...</td>
      <td>0.0270</td>
      <td>3052</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 39 columns</p>
</div>




```python
# display the rows that we have in the dataset
for row in performance.columns.values:
    print(row)
```

    algo_volatility
    algorithm_period_return
    alpha
    benchmark_period_return
    benchmark_volatility
    beta
    capital_used
    ending_cash
    ending_exposure
    ending_value
    excess_return
    gross_leverage
    information
    long_exposure
    long_value
    longs_count
    max_drawdown
    max_leverage
    net_leverage
    orders
    period_close
    period_label
    period_open
    pnl
    portfolio_value
    positions
    returns
    sharpe
    short_exposure
    short_value
    shorts_count
    sortino
    starting_cash
    starting_exposure
    starting_value
    trading_days
    transactions
    treasury_period_return
    universe_size


## Variables
Based on our algorithm assets are traded on the stock market. The algorithm works as follows: A simple algorithm that longs the top 3 stocks by Relative Strength Idex (RSI) and shorts the bottom 3 each day. The idea of RSI is to give an indicator of overbaught (i.e. overvalued) and oversold (i.e. undervalued) assets. Thus, we have the independent variable RSI, which influences the derivatives we are trading. Furthermore, the derivatives are evaluated based on other trades, which we will not consider in this analysis. The trading strategy itself is in itself a quite complex variable, as it will influence any performance measurement.

The following dependent variables will be analysed:

1. Return of the fund as daily intervals: 
   Determine overall profit/loss, mean profit/loss per time interval (day/week/month) and outliers of profit and loss
   
2. Sharpe ratio of the fund as daily intervals: 
   Determine overall Sharpe ratio (performance as compared to its risk), mean Sharpe ratio per time interval (day/week/month) and outliers
   
3. Beta of the fund as daily intervals: 
   Measure historical volatility in comparison to S&P500 index 
   
4. Alpha of the fund as daily intervals: 
   Measure historical return on investment compared to its Sharpe ratio (risk adjusted expected return)

### Return of the fund
The return of the fund is influenced by how well the strategy is able to determine assets that are increasing (for long) or decreasing (for short) in value over time.

In the figure below we are printing the algorithm relative return compared to our S&P500 benchmark.


```python
%pylab inline
figsize(12, 12)
import matplotlib.pyplot as plt

fig = plt.figure()
return_graph1 = fig.add_subplot(211)
algo_performance = plt.plot(performance.algorithm_period_return)
bench_performance = plt.plot(performance.benchmark_period_return)
plt.legend(loc=0)
plt.show()
```

    Populating the interactive namespace from numpy and matplotlib



![png](pics/output_6_1.png)


As we can see our algorithm does not outperform the benchmark. Thus, let us take a deeper look into our distribution of long and short values in the portfolio and our overall return.


```python
return_graph2 = fig.add_subplot(212)
algo_return = plt.plot(performance.ending_cash)
algo_long = plt.plot(performance.long_value)
# Take inverse of short value for comparison (by default short is always negative)
algo_short = plt.plot(-performance.short_value)
plt.legend(loc=0)
plt.show()
```


![png](pics/output_8_0.png)


As we can see from the above figure, our algorithm performs quite well at the beginning. Around mid of October we see that the value which is bound in short investments starts to increase faster then our long investments. From the benchmark in the previous figure we have seen that the overall market increases. However, the algorithm holds primarily values that predict a decreasing market. As a first result, the RSI seems not to be a very well predictor of the actual value and the market behaviour. As we ran the simulation only for 2 months, this might only be true for that period of time. In a next step, we would need to analyse it over a longer period of time and go into depths of how RSI is calculated. Since we do not use RSI in our final algorithm, we will exclude this analysis here.

### Sharpe ratio
With the Sharpe ratio we can determine the return in respect to the risk involved. The Sharpe ratio is calculated by dividing the sum of the asset return and a benchmark return (S&P500 in our case) by the standard deviation of the asset return. The higher the Sharpe ratio, the higher the return with the same risk or the lower the risk with same return.


```python
return_graph3, ax1 = plt.subplots()
ax1.plot(performance.sharpe, 'b')
plt.legend(loc=2)
ax2 = ax1.twinx()
ax2.plot(performance.algo_volatility, 'g')
ax2.plot(performance.algorithm_period_return, 'r')
ax2.plot(performance.benchmark_period_return, 'y')
plt.legend(loc=1)
plt.show()
```


![png](pics/output_11_0.png)


From the above figure we see the Sharpe ratio as well as the three components the ratio is calculated from: algo_volatility (the standard deviation of asset return), algorithm_period_return and benchmark_period_return. Our algrithm performs quite poorly in terms of Sharpe ratio as overall performance is worse than the benchmark and the volatility of the return increases over time due to our losses.

### Alpha and Beta
The alpha value expresses the performance of the fund in comparison to a benchmark. Typically a higher alpha indicates a higher profitability in comparison to the benchmark. An alpha of zero means exact performance as the benchmark, a positive value indicates outperforming the benchmark and a negative value represents underperforming the benchmark.

The beta value shows the volatility of the fund in comparison to a benchmark. The beta value baseline is one and represents the same volatility as the benchmark. A value below one indicates a lower volatility and consequently a value above one a higher volatility than the benchmark.


```python
alpha_graph, ax1 = plt.subplots()
ax1.plot(performance.alpha, 'b')
plt.legend(loc=2)
ax2 = ax1.twinx()
ax2.plot(performance.beta, 'r')
plt.legend(loc=1)
plt.show
```




    <function matplotlib.pyplot.show>




![png](pics/output_14_1.png)


The figure above shows that the alpha value is decreasing overtime and confirms our observations earlier: our algorithm performs quite poorly in comparison to the S&P500.

Our beta value stays for the whole period below one, which means that our algorithm could be independent from the market. However, as it drops below zero the beta indicates that the algorithm reacts exactly opposite to the overall market.

## Time-based Performance
Lastly, we want to analyse our performance over time in terms of daily and weekly results. Therefore our above mentioned indicators including return, Sharpe ratio, alpha and beta are put into a timely perspective.


```python
fig, axes = plt.subplots(nrows=2, ncols=2)
axes[0, 0].boxplot(performance.algorithm_period_return, showmeans=True)
axes[0, 0].set_title('Return')
axes[0, 1].boxplot(performance.sharpe, showmeans=True)
axes[0, 1].set_title('Sharpe')
axes[1, 0].boxplot(performance.alpha, showmeans=True)
axes[1, 0].set_title('Alpha')
axes[1, 1].boxplot(performance.beta, showmeans=True)
axes[1, 1].set_title('Beta')
plt.setp(axes)
plt.show()
```

    /home/nud3l/GitHub/pyfolio/pyfolio/lib/python3.4/site-packages/numpy/lib/function_base.py:3834: RuntimeWarning: Invalid value encountered in percentile
      RuntimeWarning)


    



![png](pics/output_17_2.png)



```python

```
