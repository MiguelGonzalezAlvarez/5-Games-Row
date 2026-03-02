import httpx
from datetime import datetime, timedelta
from typing import Optional, List, Any
from app.core.config import settings
from app.core.logging import logger
from app.schemas.football import (
    PremierLeagueStanding,
    PremierLeagueMatch,
    CurrentStreak,
    ChallengeStatus,
)

MANCHESTER_UNITED_ID = settings.MANCHESTER_UNITED_TEAM_ID


MOCK_STANDINGS = [
    PremierLeagueStanding(position=1, team_id=1, team_name="Liverpool", team_short_name="LIV", team_crest="https://crests.football-data.org/40.png", played_games=27, won=18, draw=5, lost=4, points=59, goals_for=60, goals_against=29, goal_difference=31, form="WDLWW"),
    PremierLeagueStanding(position=2, team_id=2, team_name="Arsenal", team_short_name="ARS", team_crest="https://crests.football-data.org/57.png", played_games=27, won=17, draw=6, lost=4, points=57, goals_for=58, goals_against=26, goal_difference=32, form="WWWDL"),
    PremierLeagueStanding(position=3, team_id=66, team_name="Manchester United", team_short_name="MUN", team_crest="https://crests.football-data.org/66.png", played_games=27, won=12, draw=6, lost=9, points=42, goals_for=36, goals_against=36, goal_difference=0, form="WWLWW"),
    PremierLeagueStanding(position=4, team_id=4, team_name="Chelsea", team_short_name="CHE", team_crest="https://crests.football-data.org/49.png", played_games=27, won=14, draw=8, lost=5, points=50, goals_for=51, goals_against=29, goal_difference=22, form="WLWWW"),
    PremierLeagueStanding(position=5, team_id=5, team_name="Manchester City", team_short_name="MCI", team_crest="https://crests.football-data.org/109.png", played_games=27, won=15, draw=4, lost=8, points=49, goals_for=59, goals_against=34, goal_difference=25, form="LWWWL"),
    PremierLeagueStanding(position=6, team_id=6, team_name="Tottenham Hotspur", team_short_name="TOT", team_crest="https://crests.football-data.org/47.png", played_games=27, won=13, draw=5, lost=9, points=44, goals_for=52, goals_against=44, goal_difference=8, form="WWLWL"),
    PremierLeagueStanding(position=7, team_id=7, team_name="Brighton & Hove Albion", team_short_name="BHA", team_crest="https://crests.football-data.org/51.png", played_games=27, won=11, draw=8, lost=8, points=41, goals_for=46, goals_against=40, goal_difference=6, form="DLWWL"),
    PremierLeagueStanding(position=8, team_id=8, team_name="Fulham", team_short_name="FUL", team_crest="https://crests.football-data.org/63.png", played_games=27, won=11, draw=5, lost=11, points=38, goals_for=38, goals_against=38, goal_difference=0, form="WLDWW"),
    PremierLeagueStanding(position=9, team_id=9, team_name="Aston Villa", team_short_name="AVL", team_crest="https://crests.football-data.org/55.png", played_games=27, won=11, draw=4, lost=12, points=37, goals_for=41, goals_against=44, goal_difference=-3, form="LLWLW"),
    PremierLeagueStanding(position=10, team_id=10, team_name="Newcastle United", team_short_name="NEW", team_crest="https://crests.football-data.org/34.png", played_games=27, won=10, draw=5, lost=12, points=35, goals_for=39, goals_against=45, goal_difference=-6, form="LWLLW"),
]


MOCK_MATCHES = [
    PremierLeagueMatch(match_id=1, utc_date="2026-03-15T15:00:00Z", status="SCHEDULED", matchday=29, home_team="Manchester United", home_team_short="MUN", home_team_crest="https://crests.football-data.org/66.png", away_team="Arsenal", away_team_short="ARS", away_team_crest="https://crests.football-data.org/57.png", home_score=0, away_score=0, is_manchester_united=True),
    PremierLeagueMatch(match_id=2, utc_date="2026-03-08T15:00:00Z", status="FINISHED", matchday=28, home_team="Leicester City", home_team_short="LEI", home_team_crest="https://crests.football-data.org/46.png", away_team="Manchester United", away_team_short="MUN", away_team_crest="https://crests.football-data.org/66.png", home_score=1, away_score=2, is_manchester_united=True),
    PremierLeagueMatch(match_id=3, utc_date="2026-03-01T15:00:00Z", status="FINISHED", matchday=27, home_team="Manchester United", home_team_short="MUN", home_team_crest="https://crests.football-data.org/66.png", away_team="Ipswich Town", away_team_short="IPS", away_team_crest="https://crests.football-data.org/64.png", home_score=3, away_score=1, is_manchester_united=True),
    PremierLeagueMatch(match_id=4, utc_date="2026-02-22T15:00:00Z", status="FINISHED", matchday=26, home_team="Manchester United", home_team_short="MUN", home_team_crest="https://crests.football-data.org/66.png", away_team="Everton", away_team_short="EVE", away_team_crest="https://crests.football-data.org/58.png", home_score=2, away_score=1, is_manchester_united=True),
    PremierLeagueMatch(match_id=5, utc_date="2026-02-15T17:30:00Z", status="FINISHED", matchday=25, home_team="Fulham", home_team_short="FUL", home_team_crest="https://crests.football-data.org/63.png", away_team="Manchester United", away_team_short="MUN", away_team_crest="https://crests.football-data.org/66.png", home_score=0, away_score=1, is_manchester_united=True),
    PremierLeagueMatch(match_id=6, utc_date="2026-02-08T15:00:00Z", status="FINISHED", matchday=24, home_team="Manchester United", home_team_short="MUN", home_team_crest="https://crests.football-data.org/66.png", away_team="Crystal Palace", away_team_short="CRY", away_team_crest="https://crests.football-data.org/52.png", home_score=1, away_score=0, is_manchester_united=True),
    PremierLeagueMatch(match_id=7, utc_date="2026-02-01T15:00:00Z", status="FINISHED", matchday=23, home_team="Manchester United", home_team_short="MUN", home_team_crest="https://crests.football-data.org/66.png", away_team="Brighton & Hove Albion", away_team_short="BHA", away_team_crest="https://crests.football-data.org/51.png", home_score=1, away_score=2, is_manchester_united=True),
    PremierLeagueMatch(match_id=8, utc_date="2026-01-25T15:00:00Z", status="FINISHED", matchday=22, home_team="Manchester United", home_team_short="MUN", home_team_crest="https://crests.football-data.org/66.png", away_team="Tottenham Hotspur", away_team_short="TOT", away_team_crest="https://crests.football-data.org/47.png", home_score=0, away_score=3, is_manchester_united=True),
]


class MemoryCache:
    """Simple in-memory cache with TTL"""
    
    def __init__(self):
        self._cache: dict = {}
    
    def get(self, key: str) -> Optional[Any]:
        if key in self._cache:
            value, expiry = self._cache[key]
            if datetime.now() < expiry:
                return value
            del self._cache[key]
        return None
    
    def set(self, key: str, value: Any, ttl_seconds: int = 300):
        expiry = datetime.now() + timedelta(seconds=ttl_seconds)
        self._cache[key] = (value, expiry)
    
    def clear(self):
        self._cache.clear()


cache = MemoryCache()


class FootballAPIService:
    def __init__(self):
        self.base_url = settings.FOOTBALL_API_BASE_URL
        self.api_key = settings.FOOTBALL_API_KEY
        self.headers = {"X-Auth-Token": self.api_key}

    async def get_standings(self, use_cache: bool = True) -> List[PremierLeagueStanding]:
        """Get Premier League standings with caching"""
        cache_key = "standings"
        
        if use_cache:
            cached = cache.get(cache_key)
            if cached:
                logger.info("Returning cached standings")
                return cached
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/competitions/PL/standings",
                    headers=self.headers,
                    timeout=30.0,
                )
                response.raise_for_status()
                data = response.json()

                standings = []
                for standing in data.get("standings", []):
                    if standing.get("type") == "TOTAL":
                        for entry in standing.get("table", []):
                            standings.append(
                                PremierLeagueStanding(
                                    position=entry.get("position"),
                                    team_id=entry.get("team", {}).get("id"),
                                    team_name=entry.get("team", {}).get("name"),
                                    team_short_name=entry.get("team", {}).get("shortName"),
                                    team_crest=entry.get("team", {}).get("crest"),
                                    played_games=entry.get("playedGames"),
                                    won=entry.get("won"),
                                    draw=entry.get("draw"),
                                    lost=entry.get("lost"),
                                    points=entry.get("points"),
                                    goals_for=entry.get("goalsFor"),
                                    goals_against=entry.get("goalsAgainst"),
                                    goal_difference=entry.get("goalDifference"),
                                    form=entry.get("form"),
                                )
                            )
                        break

                cache.set(cache_key, standings, ttl_seconds=300)
                return standings

            except httpx.HTTPError as e:
                logger.error(f"Error fetching standings: {e}")
                logger.info("Returning mock standings data")
                cache.set(cache_key, MOCK_STANDINGS, ttl_seconds=300)
                return MOCK_STANDINGS

    async def get_matches(self, matchday: Optional[int] = None) -> List[PremierLeagueMatch]:
        """Get Premier League matches"""
        cache_key = f"matches_{matchday or 'all'}"
        
        cached = cache.get(cache_key)
        if cached:
            return cached
        
        async with httpx.AsyncClient() as client:
            try:
                url = f"{self.base_url}/competitions/PL/matches"
                params = {}
                if matchday:
                    params["matchday"] = matchday

                response = await client.get(
                    url,
                    headers=self.headers,
                    params=params,
                    timeout=30.0,
                )
                response.raise_for_status()
                data = response.json()

                matches = []
                for match in data.get("matches", []):
                    home_team = match.get("homeTeam", {})
                    away_team = match.get("awayTeam", {})
                    score = match.get("score", {}).get("fullTime", {})

                    is_mu = (
                        home_team.get("id") == MANCHESTER_UNITED_ID
                        or away_team.get("id") == MANCHESTER_UNITED_ID
                    )

                    matches.append(
                        PremierLeagueMatch(
                            match_id=match.get("id"),
                            utc_date=match.get("utcDate"),
                            status=match.get("status"),
                            matchday=match.get("matchday"),
                            home_team=home_team.get("name"),
                            home_team_short=home_team.get("shortName"),
                            home_team_crest=home_team.get("crest"),
                            away_team=away_team.get("name"),
                            away_team_short=away_team.get("shortName"),
                            away_team_crest=away_team.get("crest"),
                            home_score=score.get("home") or 0,
                            away_score=score.get("away") or 0,
                            is_manchester_united=is_mu,
                        )
                    )

                cache.set(cache_key, matches, ttl_seconds=180)
                return matches

            except httpx.HTTPError as e:
                logger.error(f"Error fetching matches: {e}")
                logger.info("Returning mock matches data")
                cache.set(cache_key, MOCK_MATCHES, ttl_seconds=180)
                return MOCK_MATCHES

    async def get_manchester_united_matches(self, limit: int = 10) -> List[PremierLeagueMatch]:
        """Get Manchester United recent matches"""
        all_matches = await self.get_matches()
        mu_matches = [
            m for m in all_matches if m.is_manchester_united
        ]
        return mu_matches[:limit]

    async def get_next_manchester_united_match(self) -> Optional[PremierLeagueMatch]:
        """Get next Manchester United match"""
        cache_key = "next_mu_match"
        
        cached = cache.get(cache_key)
        if cached:
            return cached
        
        all_matches = await self.get_matches()
        for match in all_matches:
            if match.is_manchester_united and match.status == "SCHEDULED":
                cache.set(cache_key, match, ttl_seconds=3600)
                return match
        return None

    async def calculate_current_streak(self) -> CurrentStreak:
        """Calculate Manchester United's current winning streak"""
        matches = await self.get_manchester_united_matches(limit=20)

        sorted_matches = sorted(matches, key=lambda x: x.utc_date, reverse=True)

        current_streak = 0
        streak_start_date = None
        last_result = None
        
        wins_needed = 5

        for match in sorted_matches:
            if match.status != "FINISHED":
                continue

            if match.home_team == "Manchester United":
                if match.home_score > match.away_score:
                    result = "W"
                elif match.home_score < match.away_score:
                    result = "L"
                else:
                    result = "D"
            else:
                if match.away_score > match.home_score:
                    result = "W"
                elif match.away_score < match.home_score:
                    result = "L"
                else:
                    result = "D"

            if result == "W":
                if current_streak == 0:
                    streak_start_date = match.utc_date
                current_streak += 1
            else:
                break

            if current_streak >= 5:
                break

        last_result = "W" if current_streak > 0 else "L"

        next_match = await self.get_next_manchester_united_match()

        return CurrentStreak(
            current_streak=current_streak,
            is_winning=current_streak > 0,
            streak_start_date=streak_start_date,
            last_match_result=last_result,
            next_match={
                "match_id": next_match.match_id,
                "utc_date": next_match.utc_date,
                "home_team": next_match.home_team,
                "away_team": next_match.away_team,
            } if next_match else None,
        )

    async def get_historical_streaks(self) -> dict:
        """Get historical winning streaks for analysis"""
        matches = await self.get_manchester_united_matches(limit=100)
        
        all_streaks = []
        current_streak = 0
        streak_start = None
        
        sorted_matches = sorted(matches, key=lambda x: x.utc_date)
        
        for match in sorted_matches:
            if match.status != "FINISHED":
                continue
                
            if match.home_team == "Manchester United":
                result = "W" if match.home_score > match.away_score else "L" if match.home_score < match.away_score else "D"
            else:
                result = "W" if match.away_score > match.home_score else "L" if match.away_score < match.home_score else "D"
            
            if result == "W":
                if current_streak == 0:
                    streak_start = match.utc_date
                current_streak += 1
            else:
                if current_streak > 0:
                    all_streaks.append({
                        "length": current_streak,
                        "start": streak_start,
                        "end": match.utc_date
                    })
                current_streak = 0
                streak_start = None
        
        if current_streak > 0:
            all_streaks.append({
                "length": current_streak,
                "start": streak_start,
                "end": None
            })
        
        all_streaks.sort(key=lambda x: x["length"], reverse=True)
        
        return {
            "longest_streak": all_streaks[0]["length"] if all_streaks else 0,
            "total_streaks": len(all_streaks),
            "top_streaks": all_streaks[:5],
            "streaks_of_3_or_more": len([s for s in all_streaks if s["length"] >= 3])
        }

    async def get_challenge_status(self) -> ChallengeStatus:
        """Get the current challenge status"""
        challenge_start = datetime.fromisoformat(
            settings.HAIRCUT_CHALLENGE_START_DATE.replace("Z", "+00:00")
        )
        
        days_since_start = (datetime.now(challenge_start.tzinfo) - challenge_start).days
        
        streak_info = await self.calculate_current_streak()
        next_match = await self.get_next_manchester_united_match()
        
        motivational_messages = {
            0: "The haircut awaits... #StillWaiting",
            1: "One down, four to go! Keep believing! 💪",
            2: "Two in a row! History is being made! 📈",
            3: "Three wins! The end is near! ✂️",
            4: "FOUR! One more! ONE MORE! AAAAAHHH! 😱",
            5: "FREEDOM! The haircut is finally happening! 🎉",
        }

        return ChallengeStatus(
            days_since_start=days_since_start,
            current_streak=streak_info.current_streak,
            target_streak=5,
            is_challenge_complete=streak_info.current_streak >= 5,
            next_match_date=next_match.utc_date if next_match else None,
            next_match_home_team=next_match.home_team if next_match else None,
            next_match_away_team=next_match.away_team if next_match else None,
            motivational_message=motivational_messages.get(
                streak_info.current_streak, motivational_messages[0]
            ),
        )


football_service = FootballAPIService()
