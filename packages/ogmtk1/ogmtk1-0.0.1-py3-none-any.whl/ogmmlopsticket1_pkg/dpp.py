"""
Extract the raw data of target ticket

"""
def main():
    ticker = ['DOGE-USD']
    start='2018-3-1' 
    end='2023-3-17'
    # Get raw data and prepare training data
    from ogmmlopsticket1_pkg.steps.rdata import getdata
    x_train, y_train, scaled_data, training_data_len, dataset, scaler, data = getdata(ticker, start=start, end=end)
    # Model Training
    from ogmmlopsticket1_pkg.steps.train import mtrain
    model = mtrain(x_train, y_train)
    # # Prepare test data
    # from steps.tdata2 import tdata
    # x_test, y_test = tdata(scaled_data, training_data_len, dataset)
    # # Model Validation
    # from steps.validation import validation
    # prediction = validation(model, x_test, y_test, scaler, data,training_data_len)
    # Quote (external dataset)
    from ogmmlopsticket1_pkg.steps.quote import quote
    start2='2023-3-15' 
    end2='2023-3-20'
    pred_price = quote(ticker, model, scaler, start=start2, end=end2)
    # Saving data
    pred_price.to_csv('pred_price.csv', encoding='utf-8')
if __name__ == '__main__':
    main()
