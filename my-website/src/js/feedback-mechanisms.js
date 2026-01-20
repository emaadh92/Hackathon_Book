/**
 * Feedback Mechanisms for Student Comprehension Assessment
 * Implements feedback mechanisms based on the assessment integration contract
 */

class FeedbackMechanisms {
  constructor() {
    this.feedbackTemplates = {
      positive: [
        "Excellent! You clearly understand this concept.",
        "Great job! Your grasp of this topic is impressive.",
        "Well done! You've demonstrated strong comprehension.",
        "Fantastic! You've mastered this concept effectively.",
        "Perfect! Your understanding of this topic is thorough."
      ],
      constructive: [
        "Good effort! Let's review this concept to strengthen your understanding.",
        "You're on the right track! A bit more review would be helpful.",
        "Nice try! With additional practice, this will become clearer.",
        "You have the basics! Some more study will solidify this concept.",
        "Getting there! A little more focus on this area will help."
      ],
      improvement: [
        "Let's spend more time on this concept to build stronger understanding.",
        "This concept needs more attention. Try reviewing the material again.",
        "Consider revisiting this topic with additional practice.",
        "More work is needed in this area to achieve mastery.",
        "This requires further study to ensure complete comprehension."
      ]
    };

    this.misconceptionLibrary = {
      'robot_nodes': [
        'Remember: Robot nodes are like specialized departments in a company.',
        'Think of nodes as independent functions that work together.',
        'Each node has a specific responsibility in the robot system.'
      ],
      'communication_channels': [
        'Topics are for broadcasting information to multiple listeners.',
        'Services are for direct request-response interactions.',
        'Actions are for long-running operations with feedback.'
      ],
      'software_to_action': [
        'The pathway goes from high-level decisions to physical actions.',
        'Software decisions are translated through multiple layers.',
        'Each layer converts the command to a more concrete form.'
      ]
    };
  }

  /**
   * Generate personalized feedback based on assessment results
   * @param {Object} assessmentResults - Results from the assessment
   * @param {string} topicId - Current topic being assessed
   * @returns {Object} Detailed feedback
   */
  generateFeedback(assessmentResults, topicId) {
    const overallScore = assessmentResults.results?.overallScore || 0;
    const breakdown = assessmentResults.results?.breakdown || {};
    const misconceptions = assessmentResults.results?.misconceptionsDetected || [];

    // Determine feedback tone based on score
    const feedbackTone = this._determineFeedbackTone(overallScore);

    // Generate main feedback message
    const mainFeedback = this._generateMainFeedback(overallScore, feedbackTone);

    // Generate detailed feedback by category
    const categoryFeedback = this._generateCategoryFeedback(breakdown);

    // Generate misconception-specific feedback
    const misconceptionFeedback = this._generateMisconceptionFeedback(misconceptions);

    // Generate recommendations
    const recommendations = this._generateRecommendations(
      overallScore,
      breakdown,
      misconceptions,
      topicId
    );

    // Generate encouragement
    const encouragement = this._generateEncouragement(overallScore, topicId);

    return {
      overallScore: overallScore,
      feedbackTone: feedbackTone,
      mainFeedback: mainFeedback,
      categoryFeedback: categoryFeedback,
      misconceptionFeedback: misconceptionFeedback,
      recommendations: recommendations,
      encouragement: encouragement,
      timestamp: new Date().toISOString()
    };
  }

  /**
   * Determine feedback tone based on score
   * @private
   */
  _determineFeedbackTone(score) {
    if (score >= 0.9) return 'positive';
    if (score >= 0.7) return 'constructive';
    return 'improvement';
  }

  /**
   * Generate main feedback message
   * @private
   */
  _generateMainFeedback(score, tone) {
    const templates = this.feedbackTemplates[tone];
    const template = templates[Math.floor(Math.random() * templates.length)];

    return {
      message: template,
      scoreInterpretation: this._interpretScore(score)
    };
  }

  /**
   * Interpret the score for user-friendly explanation
   * @private
   */
  _interpretScore(score) {
    if (score >= 0.9) return "Outstanding understanding! You've mastered this topic.";
    if (score >= 0.8) return "Strong understanding with room for refinement.";
    if (score >= 0.7) return "Good grasp of the fundamentals.";
    if (score >= 0.6) return "Basic understanding, but needs reinforcement.";
    return "Needs significant review and practice.";
  }

  /**
   * Generate feedback by category
   * @private
   */
  _generateCategoryFeedback(breakdown) {
    const feedback = {};

    for (const [category, score] of Object.entries(breakdown)) {
      const tone = this._determineFeedbackTone(score);
      const templates = this.feedbackTemplates[tone];
      const template = templates[Math.floor(Math.random() * templates.length)];

      feedback[category] = {
        score: score,
        feedback: template,
        strength: this._assessCategoryStrength(score)
      };
    }

    return feedback;
  }

  /**
   * Assess category strength
   * @private
   */
  _assessCategoryStrength(score) {
    if (score >= 0.8) return 'strong';
    if (score >= 0.6) return 'developing';
    return 'needs_work';
  }

  /**
   * Generate feedback for detected misconceptions
   * @private
   */
  _generateMisconceptionFeedback(misconceptions) {
    const feedback = [];

    for (const misconception of misconceptions) {
      const category = this._mapMisconceptionToCategory(misconception);
      const guidance = this.misconceptionLibrary[category] || [`Review the concept of ${misconception}`];

      feedback.push({
        misconception: misconception,
        category: category,
        guidance: guidance[Math.floor(Math.random() * guidance.length)],
        resources: this._suggestResources(category)
      });
    }

    return feedback;
  }

  /**
   * Map misconception to category
   * @private
   */
  _mapMisconceptionToCategory(misconception) {
    const lowerMisconception = misconception.toLowerCase();

    if (lowerMisconception.includes('node') || lowerMisconception.includes('function')) {
      return 'robot_nodes';
    }
    if (lowerMisconception.includes('topic') || lowerMisconception.includes('service') ||
        lowerMisconception.includes('communicat')) {
      return 'communication_channels';
    }
    if (lowerMisconception.includes('action') || lowerMisconception.includes('software') ||
        lowerMisconception.includes('physical')) {
      return 'software_to_action';
    }

    return 'robot_nodes'; // default category
  }

  /**
   * Suggest resources for improvement
   * @private
   */
  _suggestResources(category) {
    const resources = {
      'robot_nodes': [
        'Review the "Robot Functions as Departments" analogy',
        'Practice identifying different robot functions',
        'Explore the interactive robot function simulator'
      ],
      'communication_channels': [
        'Study the communication patterns again',
        'Try the communication simulator exercise',
        'Work through the communication scenario exercises'
      ],
      'software_to_action': [
        'Trace the software-to-action pathway example',
        'Practice with the decision-to-action simulation',
        'Review the system integration concepts'
      ]
    };

    return resources[category] || ['Review the lesson materials'];
  }

  /**
   * Generate recommendations based on performance
   * @private
   */
  _generateRecommendations(score, breakdown, misconceptions, topicId) {
    const recommendations = [];

    // Overall recommendation based on score
    if (score >= 0.8) {
      recommendations.push({
        action: 'continue',
        priority: 'normal',
        reason: 'Good understanding demonstrated, ready to continue',
        suggestedNext: this._determineNextTopic(topicId)
      });
    } else if (score >= 0.6) {
      recommendations.push({
        action: 'review_and_continue',
        priority: 'medium',
        reason: 'Solid foundation but needs reinforcement',
        suggestedNext: [topicId, this._determineNextTopic(topicId)]
      });
    } else {
      recommendations.push({
        action: 'review_topic',
        priority: 'high',
        reason: 'Fundamental concepts need strengthening',
        suggestedNext: [topicId, topicId + '-review']
      });
    }

    // Category-specific recommendations
    for (const [category, score] of Object.entries(breakdown)) {
      if (score < 0.7) {
        recommendations.push({
          action: 'focus_area',
          priority: 'medium',
          reason: `The ${category.replace(/([A-Z])/g, ' $1').toLowerCase()} area needs attention`,
          focusOn: category,
          suggestedActivities: this._suggestCategoryActivities(category)
        });
      }
    }

    // Misconception-specific recommendations
    for (const misconception of misconceptions) {
      const category = this._mapMisconceptionToCategory(misconception);
      recommendations.push({
        action: 'address_misconception',
        priority: 'high',
        reason: `Misconception detected: ${misconception}`,
        focusOn: category,
        suggestedActivities: this._suggestMisconceptionActivities(misconception)
      });
    }

    return recommendations;
  }

  /**
   * Determine next topic based on current topic
   * @private
   */
  _determineNextTopic(currentTopicId) {
    // Map current topic to next logical topic
    const nextTopicMap = {
      'introduction': 'communication-concepts',
      'communication-concepts': 'node-topic-service-analogies',
      'node-topic-service-analogies': 'software-to-action-connection',
      'software-to-action-connection': 'robot-physical-structure',
      'robot-physical-structure': 'summary',
      'summary': 'assessment'
    };

    return nextTopicMap[currentTopicId] || 'review-material';
  }

  /**
   * Suggest activities for category improvement
   * @private
   */
  _suggestCategoryActivities(category) {
    const activities = {
      'conceptualUnderstanding': [
        'Complete additional practice problems',
        'Review concept summaries',
        'Discuss with peers or instructors'
      ],
      'analogyApplication': [
        'Practice creating your own analogies',
        'Compare different analogies for the same concept',
        'Apply analogies to new scenarios'
      ],
      'practicalConnection': [
        'Work through hands-on exercises',
        'Connect concepts to real-world examples',
        'Try interactive simulations'
      ]
    };

    return activities[category] || ['Review the material again'];
  }

  /**
   * Suggest activities for misconception resolution
   * @private
   */
  _suggestMisconceptionActivities(misconception) {
    // Generic activities for misconception resolution
    return [
      `Re-read the section on ${misconception}`,
      'Try explaining this concept in your own words',
      'Work through examples step by step',
      'Seek additional resources or ask for help'
    ];
  }

  /**
   * Generate encouragement message
   * @private
   */
  _generateEncouragement(score, topicId) {
    const topicName = this._formatTopicName(topicId);

    if (score >= 0.8) {
      return `You're making great progress with "${topicName}"! Your understanding is growing stronger.`;
    } else if (score >= 0.6) {
      return `Don't worry about the challenges with "${topicName}". Learning robotics takes time and practice.`;
    } else {
      return `Keep going with "${topicName}"! Every expert was once a beginner. Your persistence will pay off.`;
    }
  }

  /**
   * Format topic name for display
   * @private
   */
  _formatTopicName(topicId) {
    return topicId
      .replace(/-/g, ' ')
      .replace(/\b\w/g, l => l.toUpperCase());
  }

  /**
   * Create a feedback summary for instructors
   * @param {Object} assessmentResults - Full assessment results
   * @param {string} studentId - Student identifier
   * @returns {Object} Instructor feedback summary
   */
  createInstructorSummary(assessmentResults, studentId) {
    const feedback = this.generateFeedback(assessmentResults, assessmentResults.topicId || 'unknown');

    return {
      studentId: studentId,
      assessmentId: assessmentResults.assessmentId || 'unknown',
      topicId: assessmentResults.topicId || 'unknown',
      overallScore: feedback.overallScore,
      strengths: this._extractStrengths(feedback),
      weaknesses: this._extractWeaknesses(feedback),
      recommendedInterventions: this._extractInterventions(feedback),
      summary: this._createInstructorSummaryText(feedback),
      timestamp: feedback.timestamp
    };
  }

  /**
   * Extract strengths from feedback
   * @private
   */
  _extractStrengths(feedback) {
    const strengths = [];

    for (const [category, data] of Object.entries(feedback.categoryFeedback)) {
      if (data.strength === 'strong') {
        strengths.push({
          category: category,
          score: data.score,
          comment: data.feedback
        });
      }
    }

    return strengths;
  }

  /**
   * Extract weaknesses from feedback
   * @private
   */
  _extractWeaknesses(feedback) {
    const weaknesses = [];

    for (const [category, data] of Object.entries(feedback.categoryFeedback)) {
      if (data.strength === 'needs_work') {
        weaknesses.push({
          category: category,
          score: data.score,
          comment: data.feedback
        });
      }
    }

    // Add misconceptions
    for (const misData of feedback.misconceptionFeedback) {
      weaknesses.push({
        type: 'misconception',
        detail: misData.misconception,
        guidance: misData.guidance
      });
    }

    return weaknesses;
  }

  /**
   * Extract recommended interventions
   * @private
   */
  _extractInterventions(feedback) {
    return feedback.recommendations.map(rec => ({
      action: rec.action,
      priority: rec.priority,
      reason: rec.reason,
      suggestedNext: rec.suggestedNext
    }));
  }

  /**
   * Create instructor summary text
   * @private
   */
  _createInstructorSummaryText(feedback) {
    const scoreLevel = feedback.overallScore >= 0.8 ? 'Proficient' :
                     feedback.overallScore >= 0.6 ? 'Developing' : 'Needs Support';

    const summary = [
      `Student performance level: ${scoreLevel}`,
      `Overall score: ${(feedback.overallScore * 100).toFixed(1)}%`,
      `Strengths: ${feedback.categoryFeedback && Object.keys(feedback.categoryFeedback).filter(cat =>
        feedback.categoryFeedback[cat].strength === 'strong').join(', ') || 'None identified'}`,
      `Areas for improvement: ${feedback.misconceptionFeedback.map(m => m.misconception).join(', ') || 'None detected'}`
    ];

    return summary.join(' | ');
  }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = FeedbackMechanisms;
} else if (typeof window !== 'undefined') {
  window.FeedbackMechanisms = FeedbackMechanisms;
}