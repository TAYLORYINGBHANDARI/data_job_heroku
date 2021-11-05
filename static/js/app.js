    
// MAKE FUNCTIONS TO CREATE THE CHARTS


function barchart(data){
    
    //clean data
    my_x = data.map(x => x.Country)
    my_y = data.map(y => y.Emission_CO2)

    //using plotly
    var plot_data = [
        {
            x: my_x,
            y: my_y,
            type: 'bar'
        }
    ];

    var layout = {
        xaxis: {automargin: true},
        yaxis: {automargin: true}
    }

    Plotly.newPlot('chart1', plot_data, layout, { 
        responsive: true});

}



//PUT ALL GRAPHS TOGETHER AND MAKE API CALL

function getData(){

    //grab the data from the endpoint you created in flask
    d3.json("/api/data").then((json) => {

        //pass that data into the functions to create the charts

        barchart(json)

        //scatterplot(json)


    })// end d3 call

}// end function getData


// INITIATE THE getData FUNCTION WHEN PAGE LOADS
getData()

