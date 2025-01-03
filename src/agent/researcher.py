from typing import List, Dict
import logging
import asyncio 
from config import Config
import groq
from datetime import datetime
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger('crypto_analyzer.researcher')

class ResearchAgent:
    """
    Lead Research Agent that coordinates specialized AI agents and synthesizes their findings
    into comprehensive crypto market analysis.
    """
    
    def __init__(self):
        logger.debug("Initializing Lead Research Agent")
        # Initialize Groq client
        self.groq_client = groq.Groq(api_key=Config.GROQ_API_KEY)
        
        self.system_prompt = """You are a lead cryptocurrency research analyst coordinating a team of specialized AI agents.
Your role is to:
1. Synthesize insights from multiple specialized agents
2. Identify emerging trends and narratives in the crypto market
3. Present clear, actionable insights
4. Maintain objectivity and highlight both opportunities and risks
5. Focus on data-driven analysis while considering market sentiment

You have access to insights from:
- Market Analysis Agent: Technical indicators and market metrics
- Sentiment Analysis Agent: Social media and news sentiment
- Narrative Analysis Agent: Emerging themes and sector trends
- Risk Analysis Agent: Market risks and correlation analysis

Approach each analysis with:
- Clear data-driven reasoning
- Multiple perspective consideration
- Trend identification
- Risk awareness
- Clear actionable insights"""

        self.user_prompt_template = """Analyze the current crypto market situation using the following data:

Market Data:
{market_data}

Sentiment Analysis:
{sentiment_data}

Narrative Trends:
{narrative_data}

Risk Assessment:
{risk_data}

Focus on:
1. Key market trends
2. Emerging narratives
3. Risk factors
4. Sector performance
5. Notable opportunities

Provide a concise but comprehensive analysis."""

        # Initialize specialized agents (to be implemented)
        self.market_agent = None
        self.sentiment_agent = None
        self.narrative_agent = None
        self.risk_agent = None

    async def collect_agent_insights(self) -> Dict:
        """Collect insights from all specialized agents"""
        logger.info("Collecting insights from specialized agents")
        
        # Placeholder for agent data collection
        insights = {
            'market_data': {},
            'sentiment_data': {},
            'narrative_data': {},
            'risk_data': {}
        }
        
        return insights

    @retry(
        stop=stop_after_attempt(Config.ANALYSIS_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def generate_ai_analysis(self, prompt: str) -> str:
        """Generate analysis using Groq API with retry logic"""
        try:
            response = await self.groq_client.chat.completions.create(
                model=Config.AI_MODEL,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=Config.TEMPERATURE,
                max_tokens=Config.MAX_TOKENS,
                timeout=Config.SYSTEM_TIMEOUT
            )
            
            analysis = response.choices[0].message.content
            
            # Validate response
            if len(analysis) < Config.MINIMUM_ANALYSIS_LENGTH:
                raise ValueError("Analysis response too short")
                
            return analysis
            
        except Exception as e:
            logger.error(f"Error in Groq API call: {str(e)}", exc_info=True)
            raise

    async def generate_research_report(self) -> Dict:
        """Generate comprehensive research report"""
        logger.info("Generating research report")
        
        # Collect insights from specialized agents
        insights = await self.collect_agent_insights()
        
        # Format user prompt with collected data
        formatted_prompt = self.user_prompt_template.format(
            market_data=insights['market_data'],
            sentiment_data=insights['sentiment_data'],
            narrative_data=insights['narrative_data'],
            risk_data=insights['risk_data']
        )
        
        # Generate analysis using Groq
        analysis = await self.generate_ai_analysis(formatted_prompt)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'insights': insights,
            'analysis': analysis,
            'recommendations': self._extract_recommendations(analysis)
        }

    def _extract_recommendations(self, analysis: str) -> List[str]:
        """Extract key recommendations from the analysis"""
        try:
            # Ask Groq to extract recommendations
            response = self.groq_client.chat.completions.create(
                model=Config.AI_MODEL,
                messages=[
                    {"role": "system", "content": "Extract key actionable recommendations from the analysis. Format as a list."},
                    {"role": "user", "content": analysis}
                ],
                temperature=0.3,  # Lower temperature for more focused extraction
                max_tokens=1000
            )
            
            return response.choices[0].message.content.split('\n')
        except Exception as e:
            logger.error(f"Error extracting recommendations: {str(e)}", exc_info=True)
            return []

    async def run(self):
        """Execute the research pipeline"""
        logger.info("Starting research pipeline")
        try:
            report = await self.generate_research_report()
            logger.info("Research pipeline completed successfully")
            return report
        except Exception as e:
            logger.error(f"Error in research pipeline: {str(e)}", exc_info=True)
            raise

if __name__ == "__main__":
    async def main():
        agent = ResearchAgent()
        report = await agent.run()
        print(report)

    asyncio.run(main())