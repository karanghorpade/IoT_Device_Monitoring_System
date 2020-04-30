from bokeh.plotting import ColumnDataSource, figure, output_file, save, show
import random

def display_graph(s_date,e_date,mont,saal):
    start_date = int(s_date)
    end_date = int(e_date)
    selected_month = str(mont)
    selected_year = str(saal)
    days = (end_date - start_date + 1)
    
    date_list = []
    for i in range(start_date,(end_date+1)):
        date_list.append(i)

    data_dict={'date':date_list, 'month':selected_month, 'year':selected_year, 'date_range':days}
    create_graph(data_dict)



def create_graph(data_dict):
    output_file("templates\\date-range-graph.html", mode="inline")
    
    date_list = data_dict['date']
    #Generate description list
    desc_list=[]
    add_month = str(data_dict['month'])
    add_year = str(data_dict['year'])

    for date in date_list:
        desc_list.append(str(date) +" " + add_month + " " + add_year)
    
    #Generate max and min temp values
    max_list = []
    min_list = []
    degree_list = []
    for value in range(data_dict['date_range']):
        min_list.append(random.randint(-1, 15))
        max_list.append(random.randint(16, 28))
        degree_list.append('°C')
    
    source = ColumnDataSource(data=dict(
        date = date_list,
        min_temp = min_list,
        max_temp = max_list,
        desc = desc_list,
        degree=degree_list,
        
    ))
    
    TOOLTIPS = [
        ("Unit", "@degree"),
        ("Min. Temp", "@min_temp"),
        ("Max. Temp", "@max_temp"),
        ("Date", "@desc"),
    ]
    #date_lable = 
    p = figure(plot_width=800, plot_height=500, tooltips=TOOLTIPS, x_axis_label='Dates', y_axis_label='Temperatue (°C)',
               title="Temperature Data for one week")
    
    p.line('date', 'min_temp', legend="Minimum temperature values", line_width=2, line_color="blue", source=source)
    p.circle('date', 'min_temp', fill_color="white", size=8, source=source)
    
    p.line('date', 'max_temp', legend="Maximum temperature values", line_width=2, line_color="red", source=source)
    p.circle('date', 'max_temp', fill_color="white", size=8, source=source)
    
    save(p)
    
#display_graph()