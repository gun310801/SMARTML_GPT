# SMARTML Assistant

An intelligent AI-powered machine learning companion that helps you understand ML concepts, generate model specifications, and execute training pipelines with natural language interaction.

## 🌟 Features

### 🤖 AI-Powered Assistance
- **Natural Language Processing**: Ask questions about machine learning concepts in plain English
- **Intelligent Responses**: Powered by OpenAI's language models with RAG (Retrieval-Augmented Generation)
- **Context-Aware**: Maintains conversation history and provides contextual responses

### 📊 Model Management
- **Multiple ML Algorithms**: Support for SVM, Logistic Regression, and Decision Trees.
- **JSON Specifications**: Generate executable model configurations through natural language
- **Hyperparameter Tuning**: Automated grid search for optimal model parameters
- **Model Comparison**: Compare different algorithms and their performance

### 📁 Data Handling
- **CSV Upload**: Easy dataset upload through the web interface
- **Automatic Preprocessing**: Built-in data preparation and validation
- **Visualization**: Interactive charts and metrics display

### 🎨 Modern UI/UX
- **Beautiful Interface**: Modern, responsive design with gradient themes
- **Real-time Feedback**: Progress indicators and status updates
- **Conversation History**: Persistent chat sessions with export capabilities
- **Quick Actions**: Pre-defined templates for common ML tasks

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- OpenAI API key
- Docker (optional)

### Local Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd chatpdf
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   OPENAI_API_KEY=your_api_key_here
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Access the application**
   Open your browser and navigate to `http://localhost:8501`

### Docker Installation

1. **Build the Docker image**
   ```bash
   docker build -t smartml-assistant .
   ```

2. **Run the container**
   ```bash
   docker run -p 8501:8501 --env-file .env smartml-assistant
   ```

3. **Access the application**
   Open your browser and navigate to `http://localhost:8501`

## 📁 Project Structure

```
chatpdf/
├── app.py                 # Main Streamlit application
├── rag.py                 # RAG implementation for AI responses
├── runner.py              # Model training and execution engine
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── .dockerignore         # Docker ignore patterns
├── README.md             # This file
├── Datasets/             # Uploaded datasets
│   ├── breast_cancer_wisconsin.csv
│   └── Iris.csv
├── Documents/            # Knowledge base documents
│   ├── decision_tree.pdf
│   ├── decision_tree.txt
│   ├── lr.txt
│   └── svm.txt
├── JSONs/                # Model specifications
│   ├── model_parameters.json
│   └── sample.json
└── Notebooks/            # Jupyter notebooks for development
    ├── ChatGPT_Decision_Tree.ipynb
    ├── ChatGPT_LR.ipynb
    ├── ChatGPT_SVM.ipynb
    └── chatML_allFinal.ipynb
```

## 💬 Usage Examples

### Asking Questions
```
User: "What is the difference between SVM and Logistic Regression?"
SMARTML: Provides detailed explanation with examples and use cases
```

### Generating Model Specifications
```
User: "Create a SVM model for the Iris dataset"
SMARTML: Generates JSON specification with parameters
```

### Executing Models
```
User: "Run the model with hyperparameter tuning"
SMARTML: Executes training pipeline and displays results
```

### Data Analysis
```
User: "Analyze my dataset and suggest preprocessing steps"
SMARTML: Provides data insights and recommendations
```

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `OPENAI_MODEL`: OpenAI model to use (default: gpt-3.5-turbo)

The application supports three main ML algorithms:

1. **SVM (Support Vector Machine)**
   - Kernel types: linear, rbf, poly, sigmoid
   - C parameter for regularization
   - Gamma for kernel coefficient

2. **Logistic Regression**
   - C parameter for regularization
   - Solver options: lbfgs, liblinear, newton-cg
   - Max iterations

3. **Decision Tree**
   - Max depth
   - Min samples split
   - Criterion: gini, entropy

## 📊 Features in Detail

### AI-Powered Responses
- **RAG Implementation**: Uses document retrieval for context-aware responses
- **Conversation Memory**: Maintains chat history for contextual conversations
- **Natural Language Processing**: Understands complex ML queries

### Model Execution
- **Automated Training**: One-click model training with specified parameters
- **Performance Metrics**: Accuracy, classification report, confusion matrix
- **Hyperparameter Tuning**: Grid search for optimal parameters
- **Result Visualization**: Interactive charts and detailed reports

### Data Management
- **File Upload**: Drag-and-drop CSV file upload
- **Data Validation**: Automatic format checking and preprocessing
- **Multiple Datasets**: Support for various dataset formats

## 🛠️ Development

### Adding New Models
1. Update `runner.py` with new model implementation
2. Add model parameters to `JSONs/model_parameters.json`
3. Update the RAG system with model documentation

### Extending Knowledge Base
1. Add new documents to `Documents/` directory
2. Rebuild vectorstore using the sidebar button
3. Test with relevant queries

### Customizing UI
- Modify CSS styles in `app.py`
- Add new Streamlit components
- Update quick actions and templates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request


---

**🧠 SMARTML Assistant** - Making machine learning accessible to everyone through intelligent conversation.
