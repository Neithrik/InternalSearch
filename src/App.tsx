import * as React from 'react';
import './App.css';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import SendIcon from '@mui/icons-material/Send';
import LoadingButton from '@mui/lab/LoadingButton';
import { searchApi, SearchResponse } from './search.ts';


interface ResponseProps {
  data?: SearchResponse
}

function Response({ data }: ResponseProps) {
  if (!data) {
    return null;
  }

  return (<Box>
    Response: {data.response}
    <ul>
      {data.sources.map((s, i) => <li key={i}>{s}</li>)}
    </ul>
  </Box>);
}


function App() {
  const [loading, setLoading] = React.useState(false);
  const [response, setResponse] = React.useState<SearchResponse>();
  async function startSearch(question: string) {
    setLoading(true);
    const response = await searchApi(question);
    setTimeout(() => {
      showResults(response)
    }, 2000)
  }
  function showResults(response: SearchResponse) {
    setLoading(false);
    setResponse(response);
  }

  return (
    <div className="App">
      <Container maxWidth="md">
        <Typography
          align="center"
          sx={{ color: "white", paddingTop: "24px" }}
          variant="h1"
          gutterBottom>
          Search Demo
        </Typography>
        <Box
          component="form"
          noValidate
          autoComplete="off"
        >
          <TextField
            autoFocus
            fullWidth
            slotProps={{
              htmlInput: { style: { color: 'white' } }
            }}
            sx={{ marginBottom: '8px' }}
            placeholder="Enter your search query"
            variant="outlined" />
          <LoadingButton
            onClick={(e) => {
              const input = e.currentTarget.form?.querySelector('input') as HTMLInputElement;
              startSearch(input.value);
            }}
            endIcon={<SendIcon />}
            loading={loading}
            loadingPosition="end"
            variant="contained"
          >
            Search
          </LoadingButton>
        </Box>

        <Box>
          <Response data={response} />
        </Box>
      </Container>
    </div>
  );
}

export default App;
