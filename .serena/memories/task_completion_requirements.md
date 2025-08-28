# Task Completion Requirements

## When a Task is Completed

### Mandatory Validation Steps
1. **Code Quality Checks**
   - Run linting: `npm run lint` (when available)
   - Type checking: `npm run typecheck` (when available)
   - Code formatting verification

2. **Testing Requirements**
   - Run all tests: `npm run test` (when available)
   - Ensure test coverage meets standards
   - Verify integration tests pass

3. **Build Verification**
   - Execute build process: `npm run build` (when available)
   - Confirm no build errors or warnings
   - Validate output artifacts

4. **File Organization**
   - Ensure no files are saved to root directory
   - Verify proper subdirectory organization:
     - Source code in `/src`
     - Tests in `/tests`
     - Documentation in `/docs`
     - Configuration in `/config`

5. **Claude Flow Integration**
   - Run post-task hooks as specified in development guidelines
   - Update coordination memory and metrics
   - Export session metrics if applicable

## Pre-Completion Checklist
- [ ] All tests pass
- [ ] Code linting passes without errors
- [ ] Type checking passes (if applicable)
- [ ] Build completes successfully
- [ ] Files are organized in correct subdirectories
- [ ] Agent coordination hooks completed
- [ ] Session metrics exported
- [ ] Documentation updated if needed

## Error Resolution
If any validation step fails:
1. Fix the specific issue identified
2. Re-run the failed validation step
3. Continue with remaining validation steps
4. Only mark task as complete when ALL validations pass

## Quality Gates
- **Code Quality**: Must meet project standards
- **Test Coverage**: All critical paths tested
- **Integration**: Must work with existing codebase
- **Performance**: No regression in performance metrics
- **Documentation**: Changes documented appropriately

## Success Criteria
A task is considered complete only when:
- All validation steps pass
- Quality gates are satisfied
- Integration is verified
- Documentation is current
- Coordination hooks confirm completion