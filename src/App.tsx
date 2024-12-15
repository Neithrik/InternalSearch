import * as React from 'react';
import './App.css';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import SendIcon from '@mui/icons-material/Send';
import LoadingButton from '@mui/lab/LoadingButton';

interface GeneratedResponse {
  response: string,
  sources: string[]
}

interface ResponseProps {
  data: GeneratedResponse
}

function Response({ data }: ResponseProps) {
  return (<Box>
    Response: {data.response}
    <ul>
      {data.sources.map(s => <li>source</li>)}
    </ul>
  </Box>);
}

function App() {
  const [loading, setLoading] = React.useState(false);
  const [responses, setResponses] = React.useState<GeneratedResponse[]>([]);
  function startSearch() {
    setLoading(true);
    setTimeout(() => {
      showResults([{ response: "Response from [1] and [2].", sources: ["source 1", "source 2"] }])
    }, 2000)
  }
  function showResults(responses: GeneratedResponse[]) {
    setLoading(false);
    setResponses(responses);
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
            onClick={startSearch}
            endIcon={<SendIcon />}
            loading={loading}
            loadingPosition="end"
            variant="contained"
          >
            Search
          </LoadingButton>
        </Box>

        <Box>
          {responses.map((response) => (
            <Response data={response} />
          ))}
        </Box>
      </Container>
    </div>
  );
}

export default App;
