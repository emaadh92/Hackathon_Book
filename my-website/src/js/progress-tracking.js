/**
 * Progress Tracking System
 * Implements the progress tracking contract from the educational content specifications
 */

class ProgressTracker {
  constructor(userId = 'anonymous') {
    this.userId = userId;
    this.moduleId = '001-robotic-nervous-system';
    this.moduleName = 'The Robotic Nervous System';

    // Initialize progress data structure
    this.progressData = {
      completedTopics: [],
      timeSpent: 0,
      assessmentScores: {
        average: 0,
        trend: 'stable',
        history: []
      },
      conceptMastery: {
        robotNodes: 0,
        communicationChannels: 0,
        servicesAndActions: 0
      },
      recommendedNextSteps: [],
      certificationEligible: false
    };

    // Load existing progress if available
    this.loadProgress();
  }

  /**
   * Track completion of a topic
   * @param {string} topicId - Unique identifier for the topic
   * @param {number} timeSpent - Time spent on the topic in minutes
   */
  trackTopicCompletion(topicId, timeSpent = 0) {
    if (!this.progressData.completedTopics.includes(topicId)) {
      this.progressData.completedTopics.push(topicId);
    }

    // Update time spent
    this.progressData.timeSpent += timeSpent;

    // Update concept mastery based on topic
    this._updateConceptMastery(topicId);

    // Save progress
    this.saveProgress();

    return {
      topicId: topicId,
      completed: true,
      timeSpent: timeSpent
    };
  }

  /**
   * Record an assessment result
   * @param {Object} assessmentResult - Result from assessment processing
   */
  recordAssessment(assessmentResult) {
    if (assessmentResult.results) {
      const overallScore = assessmentResult.results.overallScore;

      // Add to assessment history
      this.progressData.assessmentScores.history.push({
        topicId: this.getCurrentTopic(),
        score: overallScore,
        timestamp: new Date().toISOString()
      });

      // Update average score
      this.progressData.assessmentScores.average = this._calculateAverageScore();

      // Update trend
      this.progressData.assessmentScores.trend = this._calculateTrend();

      // Update recommended next steps based on results
      if (assessmentResult.results.recommendations) {
        this.progressData.recommendedNextSteps = assessmentResult.results.recommendations;
      }

      // Check for certification eligibility
      this.progressData.certificationEligible = this._checkCertificationEligible();

      // Save progress
      this.saveProgress();
    }

    return assessmentResult;
  }

  /**
   * Get progress data for the user and module
   * @returns {Object} Progress data matching the contract specification
   */
  getUserProgress() {
    return {
      userId: this.userId,
      moduleId: this.moduleId,
      moduleName: this.moduleName,
      overallProgress: this.calculateOverallProgress(),
      completedTopics: this.progressData.completedTopics,
      timeSpent: this.progressData.timeSpent,
      assessmentScores: {
        average: this.progressData.assessmentScores.average,
        trend: this.progressData.assessmentScores.trend
      },
      conceptMastery: this.progressData.conceptMastery,
      recommendedNextSteps: this._generateRecommendedNextSteps(),
      certificationEligible: this.progressData.certificationEligible
    };
  }

  /**
   * Calculate overall progress percentage
   * @returns {number} Progress percentage (0-1)
   */
  calculateOverallProgress() {
    const totalExpectedTopics = 10; // Based on the module structure
    const completedCount = this.progressData.completedTopics.length;

    return Math.min(completedCount / totalExpectedTopics, 1);
  }

  /**
   * Calculate average assessment score
   * @private
   */
  _calculateAverageScore() {
    const history = this.progressData.assessmentScores.history;
    if (history.length === 0) return 0;

    const sum = history.reduce((acc, record) => acc + record.score, 0);
    return sum / history.length;
  }

  /**
   * Calculate assessment trend
   * @private
   */
  _calculateTrend() {
    const history = this.progressData.assessmentScores.history;
    if (history.length < 2) return 'stable';

    const recentScores = history.slice(-3).map(r => r.score);
    const earlierScores = history.slice(-6, -3).map(r => r.score);

    if (earlierScores.length === 0) return 'stable';

    const recentAvg = recentScores.reduce((a, b) => a + b, 0) / recentScores.length;
    const earlierAvg = earlierScores.reduce((a, b) => a + b, 0) / earlierScores.length;

    if (recentAvg > earlierAvg + 0.1) return 'improving';
    if (recentAvg < earlierAvg - 0.1) return 'declining';
    return 'stable';
  }

  /**
   * Update concept mastery based on topic completed
   * @private
   */
  _updateConceptMastery(topicId) {
    // Map topics to concepts and update mastery
    if (topicId.includes('node') || topicId.includes('function')) {
      this.progressData.conceptMastery.robotNodes = Math.min(
        this.progressData.conceptMastery.robotNodes + 0.2, 1.0
      );
    }

    if (topicId.includes('communication') || topicId.includes('topic')) {
      this.progressData.conceptMastery.communicationChannels = Math.min(
        this.progressData.conceptMastery.communicationChannels + 0.2, 1.0
      );
    }

    if (topicId.includes('service') || topicId.includes('action')) {
      this.progressData.conceptMastery.servicesAndActions = Math.min(
        this.progressData.conceptMastery.servicesAndActions + 0.2, 1.0
      );
    }

    // Ensure values don't exceed 1.0
    this.progressData.conceptMastery.robotNodes = Math.min(
      this.progressData.conceptMastery.robotNodes, 1.0
    );
    this.progressData.conceptMastery.communicationChannels = Math.min(
      this.progressData.conceptMastery.communicationChannels, 1.0
    );
    this.progressData.conceptMastery.servicesAndActions = Math.min(
      this.progressData.conceptMastery.servicesAndActions, 1.0
    );
  }

  /**
   * Check if user is eligible for certification
   * @private
   */
  _checkCertificationEligible() {
    const overallProgress = this.calculateOverallProgress();
    const averageScore = this.progressData.assessmentScores.average;

    // Certification requires 80% progress and 75% average score
    return overallProgress >= 0.8 && averageScore >= 0.75;
  }

  /**
   * Generate recommended next steps
   * @private
   */
  _generateRecommendedNextSteps() {
    // If we have specific recommendations from assessments, use those
    if (this.progressData.recommendedNextSteps.length > 0) {
      return this.progressData.recommendedNextSteps.map(rec => rec.topicId);
    }

    // Otherwise, suggest next logical topics
    const allModuleTopics = [
      'introduction',
      'communication-concepts',
      'node-topic-service-analogies',
      'software-to-action-connection',
      'robot-physical-structure',
      'exercises-comprehension',
      'exercises-scenario',
      'summary',
      'assessment'
    ];

    // Find first non-completed topic
    for (const topic of allModuleTopics) {
      if (!this.progressData.completedTopics.includes(topic)) {
        return [topic];
      }
    }

    // If all topics completed, suggest review or next module
    return ['review-material', 'next-module'];
  }

  /**
   * Get current topic based on completion status
   * @returns {string} Current topic ID
   */
  getCurrentTopic() {
    const allModuleTopics = [
      'introduction',
      'communication-concepts',
      'node-topic-service-analogies',
      'software-to-action-connection',
      'robot-physical-structure',
      'exercises-comprehension',
      'exercises-scenario',
      'summary',
      'assessment'
    ];

    // Find first non-completed topic
    for (const topic of allModuleTopics) {
      if (!this.progressData.completedTopics.includes(topic)) {
        return topic;
      }
    }

    // If all topics completed, return assessment
    return 'assessment';
  }

  /**
   * Save progress to localStorage
   */
  saveProgress() {
    if (typeof window !== 'undefined' && window.localStorage) {
      const progressKey = `progress_${this.userId}_${this.moduleId}`;
      const progressData = {
        ...this.progressData,
        lastUpdated: new Date().toISOString()
      };

      localStorage.setItem(progressKey, JSON.stringify(progressData));
    }
  }

  /**
   * Load progress from localStorage
   */
  loadProgress() {
    if (typeof window !== 'undefined' && window.localStorage) {
      const progressKey = `progress_${this.userId}_${this.moduleId}`;
      const savedData = localStorage.getItem(progressKey);

      if (savedData) {
        try {
          const parsedData = JSON.parse(savedData);

          // Restore progress data but keep the structure
          this.progressData = {
            ...this.progressData,
            ...parsedData
          };
        } catch (e) {
          console.warn('Could not parse saved progress data:', e);
        }
      }
    }
  }

  /**
   * Reset progress for the user
   */
  resetProgress() {
    this.progressData = {
      completedTopics: [],
      timeSpent: 0,
      assessmentScores: {
        average: 0,
        trend: 'stable',
        history: []
      },
      conceptMastery: {
        robotNodes: 0,
        communicationChannels: 0,
        servicesAndActions: 0
      },
      recommendedNextSteps: [],
      certificationEligible: false
    };

    this.saveProgress();
  }

  /**
   * Export progress data for backup or transfer
   * @returns {Object} Complete progress data
   */
  exportProgress() {
    return {
      userId: this.userId,
      moduleId: this.moduleId,
      progressData: this.progressData,
      exportedAt: new Date().toISOString()
    };
  }

  /**
   * Import progress data
   * @param {Object} importedData - Progress data to import
   */
  importProgress(importedData) {
    if (importedData.userId === this.userId && importedData.moduleId === this.moduleId) {
      this.progressData = importedData.progressData;
      this.saveProgress();
      return true;
    }
    return false;
  }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = ProgressTracker;
} else if (typeof window !== 'undefined') {
  window.ProgressTracker = ProgressTracker;
}