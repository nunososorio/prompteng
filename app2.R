R
# Setting the libraries to be used
library(shiny)
library(readxl)
library(dplyr)

# Define the UI
ui <- fluidPage(

  # App title
  titlePanel("Data Conversion App"),

  # Sidebar panel for user input
  sidebarLayout(
    sidebarPanel(

      # Input: Select the file
      fileInput("data", "Choose CSV/XLS/XLSX File",
                accept = c("text/csv",
                           "text/comma-separated-values,text/plain",
                           ".csv",
                           ".xls",
                           ".xlsx")
      ),

      # Select the cols to delete
      checkboxGroupInput("cols", "Select the columns to delete",
                         choices = NULL),

      # Check to join files
      checkboxInput("join", "Join files that completely match the first column?",
                    TRUE)

    ),

    # Show a table with the data
    mainPanel(
      tableOutput("contents")
    )
  )
)

# Define the server logic
server <- function(input, output, session) {

  # Create a reactive value for the selected file
  my_data <- reactive({
    infile <- input$data
    if (is.null(infile))
      return(NULL)
    df <- read_excel(infile$datapath)
    updateCheckboxGroupInput(session, "cols", choices = colnames(df))
    df
  })

  # Show the selected file
  output$contents <- renderTable({
    my_data()
  })
# Run the app 

shinyApp(ui = ui, server = server)

  # Create the output
  output$out <- reactive({
    infile <- my_data()
    if (is.null(infile))
      return(NULL)
    df <- infile[,!(input$cols)]
    if (input$join) {
      df <- merge(df, infile[,!(input$cols)], by="First_Col")
    }
    

```R
# Setting the libraries to be used
library(shiny)
library(readxl)
library(dplyr)

# Define the UI
ui <- fluidPage(

  # App title
  titlePanel("Data Conversion App"),

  # Sidebar panel for user input
  sidebarLayout(
    sidebarPanel(

      # Input: Select the file
      fileInput("data", "Choose CSV/XLS/XLSX File",
                accept = c("text/csv",
                           "text/comma-separated-values,text/plain",
                           ".csv",
                           ".xls",
                           ".xlsx")
      ),

      # Select the cols to delete
      checkboxGroupInput("cols", "Select the columns to delete",
                         choices = NULL),

      # Check to join files
      checkboxInput("join", "Join files that completely match the first column?",
                    TRUE)

    ),

    # Show a table with the data
    mainPanel(
      tableOutput("contents")
    )
  )
)

# Define the server logic
server <- function(input, output, session) {

  # Create a reactive value for the selected file
  my_data <- reactive({
    infile <- input$data
    if (is.null(infile))
      return(NULL)
    df <- read_excel(infile$datapath)
    updateCheckboxGroupInput(session, "cols", choices = colnames(df))
    df
  })

  # Show the selected file
  output$contents <- renderTable({
    my_data()
  })

  # Create the output
  output$out <- reactive({
    infile <- my_data()
    if (is.null(infile))
      return(NULL)
    df <- infile[,!(input$cols)]
    if (input$join) {
      df <- merge(df, infile[,!(input$cols)], by="First_Col")
    }
    write.table(df, file="my_data.tsv", sep="\t
# Run the app 
shinyApp(ui = ui, server = server)
