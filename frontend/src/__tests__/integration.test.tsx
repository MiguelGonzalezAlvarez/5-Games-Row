import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, waitFor, act } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
      cacheTime: 0,
    },
  },
});

const wrapper = ({ children }: { children: React.ReactNode }) => (
  <QueryClientProvider client={queryClient}>
    <BrowserRouter>
      {children}
    </BrowserRouter>
  </QueryClientProvider>
);

import HaircutCounter from '../components/haircut/HaircutCounter';
import MatchPredictor from '../components/predictor/MatchPredictor';
import LeagueTable from '../components/premier-league/LeagueTable';
import ManchesterMatches from '../components/premier-league/ManchesterMatches';
import HistoricalStats from '../components/premier-league/HistoricalStats';

vi.mock('../utils/api', () => ({
  api: {
    getChallengeStatus: vi.fn(),
    getStandings: vi.fn(),
    getManchesterUnitedMatches: vi.fn(),
    getMatches: vi.fn(),
  },
}));

vi.mock('../utils/websocket', () => ({
  useWebSocket: vi.fn(() => ({
    isConnected: false,
    lastMessage: null,
    sendMessage: vi.fn(),
    connect: vi.fn(),
    disconnect: vi.fn(),
  })),
  useChallengeUpdates: vi.fn(),
  useMatchUpdates: vi.fn(),
  useStandingsUpdates: vi.fn(),
}));

const { api } = require('../utils/api');

describe('HaircutCounter Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    queryClient.clear();
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  it('renders loading state initially', async () => {
    api.getChallengeStatus.mockImplementation(
      () => new Promise(() => {})
    );

    render(<HaircutCounter />, { wrapper });
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  it('renders challenge data when loaded', async () => {
    api.getChallengeStatus.mockResolvedValue({
      days_since_start: 500,
      current_streak: 3,
      target_streak: 5,
      is_challenge_complete: false,
      motivational_message: 'Three wins! The end is near!',
      next_match_date: '2026-03-15T15:00:00Z',
      next_match_home_team: 'Manchester United',
      next_match_away_team: 'Aston Villa',
    });

    render(<HaircutCounter />, { wrapper });

    await waitFor(() => {
      expect(screen.getByText('500')).toBeInTheDocument();
    });
  });

  it('renders error state on failure', async () => {
    api.getChallengeStatus.mockRejectedValue(new Error('Network error'));

    render(<HaircutCounter />, { wrapper });

    await waitFor(() => {
      expect(screen.getByText(/failed to load/i)).toBeInTheDocument();
    });
  });

  it('displays motivational message', async () => {
    api.getChallengeStatus.mockResolvedValue({
      days_since_start: 100,
      current_streak: 2,
      target_streak: 5,
      is_challenge_complete: false,
      motivational_message: 'Two in a row!',
      next_match_date: null,
      next_match_home_team: null,
      next_match_away_team: null,
    });

    render(<HaircutCounter />, { wrapper });

    await waitFor(() => {
      expect(screen.getByText(/two in a row/i)).toBeInTheDocument();
    });
  });
});

describe('LeagueTable Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    queryClient.clear();
  });

  it('renders loading state', async () => {
    api.getStandings.mockImplementation(() => new Promise(() => {}));

    render(<LeagueTable />, { wrapper });
    expect(screen.getByText(/loading standings/i)).toBeInTheDocument();
  });

  it('renders standings data', async () => {
    api.getStandings.mockResolvedValue([
      {
        position: 1,
        team_id: 1,
        team_name: 'Arsenal',
        team_short_name: 'ARS',
        team_crest: 'https://example.com/crest.png',
        played_games: 25,
        won: 18,
        draw: 5,
        lost: 2,
        points: 59,
        goals_for: 60,
        goals_against: 25,
        goal_difference: 35,
        form: 'WWWDLW'
      },
      {
        position: 2,
        team_id: 66,
        team_name: 'Manchester United',
        team_short_name: 'MUN',
        team_crest: 'https://example.com/mun.png',
        played_games: 25,
        won: 15,
        draw: 5,
        lost: 5,
        points: 50,
        goals_for: 45,
        goals_against: 30,
        goal_difference: 15,
        form: 'WLWWL'
      }
    ]);

    render(<LeagueTable />, { wrapper });

    await waitFor(() => {
      expect(screen.getByText('Arsenal')).toBeInTheDocument();
      expect(screen.getByText('Manchester United')).toBeInTheDocument();
    });
  });

  it('highlights Manchester United', async () => {
    api.getStandings.mockResolvedValue([
      {
        position: 4,
        team_id: 66,
        team_name: 'Manchester United',
        team_short_name: 'MUN',
        team_crest: 'https://example.com/mun.png',
        played_games: 25,
        won: 15,
        draw: 5,
        lost: 5,
        points: 50,
        goals_for: 45,
        goals_against: 30,
        goal_difference: 15,
        form: 'WLWWL'
      }
    ]);

    render(<LeagueTable />, { wrapper });

    await waitFor(() => {
      const muRow = screen.getByText('Manchester United').closest('tr');
      expect(muRow).toHaveClass('highlight');
    });
  });
});

describe('MatchPredictor Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders match predictor', () => {
    render(<MatchPredictor />, { wrapper });
    expect(screen.getByText(/match predictor/i)).toBeInTheDocument();
  });

  it('renders team names', () => {
    render(<MatchPredictor />, { wrapper });
    expect(screen.getByText('Man United')).toBeInTheDocument();
    expect(screen.getByText('Aston Villa')).toBeInTheDocument();
  });

  it('renders score inputs', () => {
    render(<MatchPredictor />, { wrapper });
    const inputs = screen.getAllByRole('spinbutton');
    expect(inputs).toHaveLength(2);
  });

  it('updates home score when plus button clicked', async () => {
    const user = userEvent.setup();
    render(<MatchPredictor />, { wrapper });

    const plusButtons = screen.getAllByRole('button', { name: '+' });
    await user.click(plusButtons[0]);

    const inputs = screen.getAllByRole('spinbutton');
    expect(inputs[0]).toHaveValue(3);
  });

  it('updates away score when minus button clicked', async () => {
    const user = userEvent.setup();
    render(<MatchPredictor />, { wrapper });

    const minusButtons = screen.getAllByRole('button', { name: '-' });
    await user.click(minusButtons[1]);

    const inputs = screen.getAllByRole('spinbutton');
    expect(inputs[1]).toHaveValue(0);
  });

  it('submits prediction', async () => {
    const user = userEvent.setup();
    render(<MatchPredictor />, { wrapper });

    const submitButton = screen.getByRole('button', { name: /submit prediction/i });
    await user.click(submitButton);

    expect(screen.getByText(/your prediction/i)).toBeInTheDocument();
  });

  it('allows changing prediction after submit', async () => {
    const user = userEvent.setup();
    render(<MatchPredictor />, { wrapper });

    const submitButton = screen.getByRole('button', { name: /submit prediction/i });
    await user.click(submitButton);

    const changeButton = screen.getByRole('button', { name: /change prediction/i });
    await user.click(changeButton);

    expect(screen.getByRole('button', { name: /submit prediction/i })).toBeInTheDocument();
  });
});

describe('ManchesterMatches Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    queryClient.clear();
  });

  it('renders loading state', async () => {
    api.getManchesterUnitedMatches.mockImplementation(() => new Promise(() => {}));

    render(<ManchesterMatches />, { wrapper });
    expect(screen.getByText(/loading matches/i)).toBeInTheDocument();
  });

  it('renders match data', async () => {
    api.getManchesterUnitedMatches.mockResolvedValue([
      {
        match_id: 1,
        utc_date: '2026-03-10T15:00:00Z',
        status: 'FINISHED',
        matchday: 29,
        home_team: 'Manchester United',
        home_team_short: 'MUN',
        home_team_crest: 'https://example.com/mun.png',
        away_team: 'Arsenal',
        away_team_short: 'ARS',
        away_team_crest: 'https://example.com/ars.png',
        home_score: 2,
        away_score: 1,
        is_manchester_united: true
      }
    ]);

    render(<ManchesterMatches />, { wrapper });

    await waitFor(() => {
      expect(screen.getByText('Man United')).toBeInTheDocument();
      expect(screen.getByText('Arsenal')).toBeInTheDocument();
    });
  });
});

describe('HistoricalStats Component', () => {
  it('renders historical stats', () => {
    render(<HistoricalStats />, { wrapper });
    expect(screen.getByText(/historical streaks/i)).toBeInTheDocument();
  });

  it('renders stats after loading', async () => {
    render(<HistoricalStats />, { wrapper });

    await waitFor(() => {
      expect(screen.getByText('4')).toBeInTheDocument();
      expect(screen.getByText('12')).toBeInTheDocument();
    });
  });
});

describe('Error Handling', () => {
  it('handles API errors gracefully', async () => {
    api.getChallengeStatus.mockRejectedValue(new Error('API Error'));

    render(<HaircutCounter />, { wrapper });

    await waitFor(() => {
      expect(screen.getByText(/failed to load/i)).toBeInTheDocument();
    });
  });
});

describe('Component Interactions', () => {
  it('multiple components can render together', async () => {
    api.getChallengeStatus.mockResolvedValue({
      days_since_start: 500,
      current_streak: 3,
      target_streak: 5,
      is_challenge_complete: false,
      motivational_message: 'Test message',
      next_match_date: null,
      next_match_home_team: null,
      next_match_away_team: null,
    });

    api.getManchesterUnitedMatches.mockResolvedValue([]);

    const { rerender } = render(<HaircutCounter />, { wrapper });
    
    await waitFor(() => {
      expect(screen.getByText('500')).toBeInTheDocument();
    });

    rerender(<ManchesterMatches />);

    await waitFor(() => {
      expect(screen.getByText(/recent matches/i)).toBeInTheDocument();
    });
  });
});
