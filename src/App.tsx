import * as React from 'react';
import './App.css';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import SendIcon from '@mui/icons-material/Send';
import LoadingButton from '@mui/lab/LoadingButton';
import Link from '@mui/material/Link';
import { searchApi, SearchResponse } from './search.ts';
import Skeleton from '@mui/material/Skeleton';

interface ResponseProps {
  data?: SearchResponse;
  loading?: boolean;
}

function ResponseSkeleton() {
  return (
    <Box className="response-container">
      {/* Response text skeleton */}
      <Skeleton variant="text" sx={{ fontSize: '1rem', mb: 1 }} />
      <Skeleton variant="text" sx={{ fontSize: '1rem', mb: 1 }} />
      <Skeleton variant="text" sx={{ fontSize: '1rem', mb: 3 }} width="60%" />

      {/* Sources skeleton */}
      <Box className="sources-container">
        <Typography variant="subtitle2" color="textSecondary">Sources:</Typography>
        {[1, 2].map((_, i) => (
          <Box key={i} className="source-item">
            <Box className="source-number">[{i + 1}]</Box>
            <Skeleton variant="text" sx={{ fontSize: '0.875rem' }} width="80%" />
          </Box>
        ))}
      </Box>
    </Box>
  );
}

function Response({ data, loading }: ResponseProps) {
  const [hoveredCitation, setHoveredCitation] = React.useState<number | null>(null);

  React.useEffect(() => {
    const handleCitationHover = (event: CustomEvent) => {
      setHoveredCitation(event.detail);
    };

    document.addEventListener('citation-hover', handleCitationHover as EventListener);
    return () => {
      document.removeEventListener('citation-hover', handleCitationHover as EventListener);
    };
  }, []);

  if (loading) {
    return <ResponseSkeleton />;
  }

  if (!data) {
    return null;
  }

  const formatResponseWithCitations = (text: string) => {
    let formattedText = text;
    data.sources.forEach((_, index) => {
      const citationNumber = index + 1;
      const regex = new RegExp(`\\[${citationNumber}\\]`, 'g'); // 'g' flag for global replacement
      formattedText = formattedText.replace(
        regex,
        `<span 
          class="citation-number" 
          data-citation="${citationNumber}"
          onmouseover="this.dispatchEvent(new CustomEvent('citation-hover', {detail: ${citationNumber}}))"
          onmouseout="this.dispatchEvent(new CustomEvent('citation-hover', {detail: null}))"
        >${citationNumber}</span>`
      );
    });
    return formattedText;
  };

  return (
    <Box className="response-container">
      <Typography
        variant="body1"
        className="response-text"
        dangerouslySetInnerHTML={{ __html: formatResponseWithCitations(data.response) }}
      />
      <Box className="sources-container">
        <Typography variant="subtitle2" color="textSecondary">Sources:</Typography>
        {data.sources.map((s, i) => (
          <Box
            key={i}
            className={`source-item ${hoveredCitation === i + 1 ? 'highlighted' : ''}`}
          >
            <Box className="source-number">[{i + 1}]</Box>
            <Link
              href={s}
              target="_blank"
              rel="noopener noreferrer"
              className="source-link"
            >
              <Typography variant="body2">{s}</Typography>
            </Link>
          </Box>
        ))}
      </Box>
    </Box>
  );
}

function App() {
  const [loading, setLoading] = React.useState(false);
  const [response, setResponse] = React.useState<SearchResponse>();
  const [searchQuery, setSearchQuery] = React.useState('');

  async function startSearch(question: string) {
    if (!question.trim()) return;

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

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    startSearch(searchQuery);
  };

  return (
    <div className="App">
      <Container maxWidth="lg">
        <Box className="content-wrapper">
          <Box className="header-container">
            <Typography
              align="left"
              className="app-title"
              variant="h4"
              gutterBottom>
              Synthesia Search
            </Typography>
          </Box>

          <Box className="search-container">
            <Box
              component="form"
              noValidate
              autoComplete="off"
              className="search-form"
              onSubmit={handleSubmit}
            >
              <TextField
                autoFocus
                fullWidth
                className="search-input"
                placeholder="Ask anything..."
                variant="outlined"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
              <LoadingButton
                type="submit"
                endIcon={<SendIcon />}
                loading={loading}
                loadingPosition="end"
                variant="contained"
                className="search-button"
              >
                Search
              </LoadingButton>
            </Box>
          </Box>

          <Box className="results-container">
            <Response data={response} loading={loading} />
          </Box>
        </Box>
      </Container>
    </div>
  );
}

export default App;
