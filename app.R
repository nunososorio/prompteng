
# Library setup
library(shiny)
library(readxl)
library(write_tsv)

# UI
ui <- fluidPage(
  # Inputs
  textInput("filePath", "File Path"),
  radioButtons("fileType", "File Type", 
               c("xls" = "xls",
                 "xlsx" = "xlsx")),
  textInput("colRemove", "Columns to Remove (comma separated)"),
  textInput("filesCompare", "Files to Compare (comma separated)"),
  textInput("combineFile", "File to Combine With (optional)"),
  # Output
  textInput("outputPath", "Output Path")
)

# Server
server <- function(input, output) {
  # Read in file
  file <- read_excel(input$filePath, 
                     sheet = input$fileType)
  
  # Remove columns from file
  file <- file[, -which(colnames(file) %in% unlist(strsplit(input$colRemove, ",")))]
  
  # Compare first columns of two or more files
  compare <- lapply(strsplit(input$filesCompare, ","), function(x) 
    identical(file[, 1], read_excel(x, sheet = input$fileType)[, 1]))
  
  # Combine files based on matching first columns
  if (input$combineFile != "") {
    file <- merge(file, read_excel(input$combineFile, sheet = input$fileType),
                  by = "V1", all = TRUE)
  }
  
  # Write to tsv
  write_tsv(file, path = input$outputPath)
}

# Run Shiny app
shinyApp(ui = ui, server = server)
