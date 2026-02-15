def get_style():
    return """
        <style>
        h1, h2, h3  {
            font-family: sans-serif !important;
            font-weight: 150 !important;
            color: #008a6b !important;
        }
        div {
            font-size: 14px !important;
            font-weight: 450;
        }

        
        .stApp {
            background-color: #C8E6C9 !important;
        }

        .stSidebar {
            background-color: #B8DDB9 !important;
        }
        .stAppHeader {
            background-color: #C8E6C9 !important;
        }
        .stAppHeader::before {
            content: "Raging Roundabout In Auckland";
            position: absolute;
            left: 24px;
            top: 50%;
            transform: translateY(-50%) scaleY(0.85);
            font-size: 24px;
            font-weight: bold;
            color: #008a6b;
        }
        .stMarkdown div {
            font-size: 14px !important;
            font-weight: 350;
        }
        .st-emotion-cache-dqk60d { /* sidebar selectbox titles */
            color: #008a6b;
        }
        </style>
    """
